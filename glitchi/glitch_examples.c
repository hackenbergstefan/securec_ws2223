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
      : "+w"(cnt));
  trigger_low();
  simpleserial_put(0x01, 2, (uint8_t *)&cnt);
  return 0;
}

uint8_t example2(uint8_t cmd, uint8_t scmd, uint8_t len, uint8_t *pw) {
  trigger_high();
  asm("nop\n"
      "nop\n"
      "nop\n"
      "nop\n"
      "nop\n");

  uint8_t ret = 0x00;
  uint16_t foo = (uint16_t)0 - (pw[0] ^ 0x55);
  foo >>= 15;
  ret ^= 0x0f * (uint8_t)(1 - foo);
  foo = (uint16_t)0 - (pw[1] ^ 0x66);
  foo >>= 15;
  ret ^= 0xa0 * (uint8_t)(1 - foo);
  // if (pw[0] == 0x55) {
  //   ret ^= 0x0f;
  // }
  // if (pw[1] == 0x66) {
  //   ret ^= 0xa0;
  // }

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
  simpleserial_addcmd(0x02, 2, example2);
  while (1)
    simpleserial_get();
}
