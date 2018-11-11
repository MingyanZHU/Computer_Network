/*
    * THIS FILE IS FOR IP TEST
    * IPV4 分组收发实验部分
    */
// system support
#include "sysInclude.h"
#include <stdio.h>
#include <malloc.h>
extern void ip_DiscardPkt(char *pBuffer, int type);

extern void ip_SendtoLower(char *pBuffer, int length);

extern void ip_SendtoUp(char *pBuffer, int length);

extern unsigned int getIpv4Address();

// implemented by students

int stud_ip_recv(char *pBuffer, unsigned short length)
{
    int version = pBuffer[0] >> 4;                             // 0 byte first 4 bits ip version
    int head_length = pBuffer[0] & 0xf;                        // 0 byte last 4 bits  head length
    short ttl = (unsigned short)pBuffer[8];                    // 8 byte all 8 bits ttl
    short checksum = ntohs(*(unsigned short *)(pBuffer + 10)); // 10 byte all 8 bits
    int destination = ntohl(*(unsigned int *)(pBuffer + 16));  // 16 byte 4 Bytes destination ip

    if (ttl == 0)
    {
        // TTL error
        ip_DiscardPkt(pBuffer, STUD_IP_TEST_TTL_ERROR);
        return 1;
    }
    if (version != 4)
    {
        // version is not 4
        ip_DiscardPkt(pBuffer, STUD_IP_TEST_VERSION_ERROR);
        return 1;
    }
    if (head_length < 5)
    {
        // head length is not 20 bytes
        ip_DiscardPkt(pBuffer, STUD_IP_TEST_HEADLEN_ERROR);
        return 1;
    }
    if (destination != getIpv4Address() && destination != 0xffff)
    {
        ip_DiscardPkt(pBuffer, STUD_IP_TEST_DESTINATION_ERROR);
        return 1;
    }
    unsigned long sum = 0;
    unsigned long temp = 0;
    int i;
    for (i = 0; i < head_length * 2; i++)
    {
        temp += (unsigned char)pBuffer[i * 2] << 8;
        temp += (unsigned char)pBuffer[i * 2 + 1];
        sum += temp;
        temp = 0;
    }
    unsigned short l_word = sum & 0xffff;
    unsigned short h_word = sum >> 16;
    if (l_word + h_word != 0xffff)
    {
        ip_DiscardPkt(pBuffer, STUD_IP_TEST_CHECKSUM_ERROR);
        return 1;
    }

    ip_SendtoUp(pBuffer, length);
    return 0;
}

int stud_ip_Upsend(char *pBuffer, unsigned short len, unsigned int srcAddr,
                   unsigned int dstAddr, byte protocol, byte ttl)
{
    // 默认头部长度为20Bytes
    short ip_length = len + 20;
    char *buffer = (char *)malloc(ip_length * sizeof(char));
    memset(buffer, 0, ip_length);
    buffer[0] = 0x45;
    buffer[8] = ttl;
    buffer[9] = protocol;
    // 转换为网络字节序
    unsigned short network_length = htons(ip_length);
    // buffer[2] = network_length >> 8;
    // buffer[3] = network_length & 0xff;
    memcpy(buffer + 2, &network_length, 2);
    unsigned int src = htonl(srcAddr);
    unsigned int dst = htonl(dstAddr);

    memcpy(buffer + 12, &src, 4);
    memcpy(buffer + 16, &dst, 4);

    unsigned long sum = 0;
    unsigned long temp = 0;
    int i;
    for (i = 0; i < 20; i += 2)
    {
        temp += (unsigned char)buffer[i] << 8;
        temp += (unsigned char)buffer[i + 1];
        sum += temp;
        temp = 0;
    }
    unsigned short l_word = sum & 0xffff;
    unsigned short h_word = sum >> 16;
    unsigned short checksum = l_word + h_word;
    checksum = ~checksum;
    unsigned short header_checksum = htons(checksum);
    // buffer[10] = header_checksum >> 8;
    // buffer[11] = header_checksum & 0xff;
    memcpy(buffer + 10, &header_checksum, 2);
    memcpy(buffer + 20, pBuffer, len);
    // ip_SendtoLower(buffer, ip_length);
    ip_SendtoLower(buffer, len + 20);
    return 0;
}
