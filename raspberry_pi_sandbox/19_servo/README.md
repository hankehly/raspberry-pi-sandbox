
- [Lesson 19](https://www.youtube.com/watch?v=i7hMx6YLR0Q&list=PLGs0VKk2DiYxdMjCJmcP6jt4Yw6OHK85O&index=22&ab_channel=PaulMcWhorter)
- [Servo](https://docs.sunfounder.com/projects/raphael-kit/en/latest/components/component_servo.html)
- [Fixing the jitter](https://www.youtube.com/watch?v=mARXLF5cnKE&ab_channel=LoriPfahler)

Warning
* Directly driving the server from the Raspberry Pi will use too much power and will cause the Raspberry Pi to reboot. Try using an external power supply for the servo.
* pigpio only accepts BCM numbering.


```bash
sudo systemctl enable pigpiod
```
