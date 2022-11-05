#include <stddef.h>
#include <stdint.h>

static const uint8_t stored_password[] = "infineon";

void print_buffer(uint8_t *buffer, size_t length);

uint8_t password_wrong;

void setup(uint8_t *input)
{
    password_wrong = 0;
}

void run(uint8_t *input)
{
    for (unsigned int i = 0; i < sizeof(stored_password) - 1; i++)
    {
        if (stored_password[i] != input[i])
        {
            password_wrong = 1;
            break;
        }
    }
}

void teardown()
{
    print_buffer(&password_wrong, sizeof(password_wrong));
}
