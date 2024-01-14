### FLASK CTF 개발

![image](https://github.com/BoB12-sumin/ruddus/assets/66521935/b6ee5d41-992f-4866-927e-1bc823051ecf)

#### 같은 내부망에 있는 공격자가 해당 PC로 DOS공격을 시도했다. DOS 공격의 종류와, 공격자는 누구인지 찾는다.

- [ ] hint: 서비스 거부 공격 https://ko.wikipedia.org/wiki/%EC%84%9C%EB%B9%84%EC%8A%A4_%EA%B1%B0%EB%B6%80_%EA%B3%B5%EA%B2%A9
- [ ] hint2: allow command, ["tcpdump", "ls", "arp", "ifconfig", "ping", "time"]
- [x] Dos 공격중 일 때에는 인터넷과 시스템 동작이 잘 되지 않거나 속도가 느리다.
      ex) ping 패킷이 손실되거나 반응속도가 느리다.
