/*
* THIS FILE IS FOR IP FORWARD TEST
* IPV4 分组收发实验部分
*/
#include "sysInclude.h"
#include <stdio.h>
#include <vector>
using std::vector;
// system support
extern void fwd_LocalRcv(char *pBuffer, int length);

extern void fwd_SendtoLower(char *pBuffer, int length, unsigned int nexthop);

extern void fwd_DiscardPkt(char *pBuffer, int type);

extern unsigned int getIpv4Address();

// implemented by students

vector<stud_route_msg> route;

void stud_Route_Init()
{
	// Global route info?
	return;
}

void stud_route_add(stud_route_msg *proute)
{

	stud_route_msg temp;
	unsigned int dest = ntohl(proute->dest);
	unsigned int masklen = ntohl(proute->masklen); // 24 extra
	unsigned int nexthop = ntohl(proute->nexthop);
	temp.dest = dest;
	temp.masklen = masklen;
	temp.nexthop = nexthop;
	route.push_back(temp);
	return;
}

int stud_fwd_deal(char *pBuffer, int length)
{
	int version = pBuffer[0] >> 4;							   // 0 byte first 4 bits ip version
	int head_length = pBuffer[0] & 0xf;						   // 0 byte last 4 bits  head length
	short ttl = (unsigned short)pBuffer[8];					   // 8 byte all 8 bits ttl
	short checksum = ntohs(*(unsigned short *)(pBuffer + 10)); // 10 byte all 8 bits
	int destination = ntohl(*(unsigned int *)(pBuffer + 16));  // 16 byte 4 Bytes destination ip

	// ttl -= 1;

	if (ttl <= 0)
	{
		// TTL error
		fwd_DiscardPkt(pBuffer, STUD_FORWARD_TEST_TTLERROR);
		return 1;
	}

	if (destination == getIpv4Address())
	{
		fwd_LocalRcv(pBuffer, length);
		return 0;
	}

	stud_route_msg *ans_route = NULL;
	int temp_dest = destination;
	for (int i = 0; i < route.size(); i++)
	{
		unsigned int temp_sub_net = route[i].dest & ((1 << 31) >> (route[i].masklen - 1));

		if (temp_sub_net == temp_dest)
		{
			ans_route = &route[i];
			break;
		}
	}

	if (!ans_route)
	{
		fwd_DiscardPkt(pBuffer, STUD_FORWARD_TEST_NOROUTE);
		return 1;
	}
	else
	{
		char *buffer = new char[length];
		memcpy(buffer, pBuffer, length);
		buffer[8] = ttl - 1;
		memset(buffer + 10, 0, 2);
		unsigned long sum = 0;
		unsigned long temp = 0;

		for (int i = 0; i < head_length * 2; i++)
		{
			temp += (unsigned char)buffer[i * 2] << 8;
			temp += (unsigned char)buffer[i * 2 + 1];
			sum += temp;
			temp = 0;
		}
		unsigned short l_word = sum & 0xffff;
		unsigned short h_word = sum >> 16;
		unsigned short checksum = l_word + h_word;
		checksum = ~checksum;
		unsigned short header_checksum = htons(checksum);
		memcpy(buffer + 10, &header_checksum, 2);
		fwd_SendtoLower(buffer, length, ans_route->nexthop);
	}
	return 0;
}
