#include <stddef.h>
#include <stdint.h>

static const uint8_t stored_password[] = "infineon";

extern uint8_t *input;
void print_buffer(uint8_t *buffer, size_t length);

uint8_t password_correct;

void setup(uint8_t *input)
{
    password_correct = 0;
}

void run(void)
{
    for (unsigned int i = 0; i < sizeof(stored_password) - 1; i++)
    {
        if (stored_password[i] != input[i])
        {
            password_correct = 1;
            break;
        }
    }
}

void teardown()
{
    print_buffer(&password_correct, sizeof(password_correct));
}
