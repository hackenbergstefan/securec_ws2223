#include "hal.h"
#include <stdint.h>
#include <stdlib.h>

#include "simpleserial.h"

uint8_t example1(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *in) {
  uint16_t cnt = 0xaf00;
  trigger_high();
  asm("nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "ori %0, 0x01 \n"
      "ori %0, 0x02 \n"
      "ori %0, 0x04 \n"
      "ori %0, 0x08 \n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      : "+w"(cnt));
  trigger_low();
  simpleserial_put(0x01, 2, (uint8_t *)&cnt);
  return 0;
}

uint8_t example2(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *in) {
  uint16_t cnt = 0xaf00;
  *(volatile uint16_t *)in = cnt;
  trigger_high();
  asm("nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "adiw %0, 0x03 \n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      : "+w"(cnt));
  trigger_low();
  *(uint16_t *)in = cnt;
  simpleserial_put(0x01, 2, in);
  return 0;
}

uint8_t example3(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *pw) {
  trigger_high();
  asm("nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n");

  uint8_t ret = 0x00;
  if (pw[0] == 0x55) {
    ret ^= 0x0f;
  }
  if (pw[1] == 0x66) {
    ret ^= 0xa0;
  }

  asm("nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n");

  trigger_low();

  simpleserial_put(0x01, 1, (uint8_t *)&ret);
  return 0x00;
}

int main(void) {
  platform_init();
  init_uart();
  trigger_setup();

  simpleserial_init();
  simpleserial_addcmd(0x01, 0, example1);
  simpleserial_addcmd(0x02, 0, example2);
  simpleserial_addcmd(0x03, 2, example3);
  while (1)
    simpleserial_get();
}
