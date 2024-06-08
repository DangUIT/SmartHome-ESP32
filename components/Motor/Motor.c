#include <stdio.h>
#include "Motor.h"
#include "driver/ledc.h"
#include "esp_err.h"

#define LEDC_TIMER              LEDC_TIMER_0
#define LEDC_MODE               LEDC_LOW_SPEED_MODE
#define LEDC_OUTPUT_IO          (17) // Define the output GPIO

// #define LEDC_OUTPUT_IN1         (16) // Define the output GPIO
// #define LEDC_OUTPUT_IN2         (4) // Define the output GPIO


#define LEDC_CHANNEL            LEDC_CHANNEL_0


#define LEDC_DUTY_RES           LEDC_TIMER_13_BIT // Set duty resolution to 13 bits
// #define LEDC_DUTY               (0000) // Set duty to 50%. (2 ** 13) * 50% = 4096
#define LEDC_FREQUENCY          (5000) // Frequency in Hertz. Set frequency at 5 kHz

/* Warning:
 * For ESP32, ESP32S2, ESP32S3, ESP32C3 targets,
 * when LEDC_DUTY_RES selects the maximum duty resolution (i.e. value equal to SOC_LEDC_TIMER_BIT_WIDTH),
 * 100% duty cycle is not reachable (duty cannot be set to (2 ** SOC_LEDC_TIMER_BIT_WIDTH)).
 */

static void example_ledc_init(void)
{
    // Prepare and then apply the LEDC PWM timer configuration
    ledc_timer_config_t ledc_timer = {
        .speed_mode       = LEDC_MODE,
        .timer_num        = LEDC_TIMER,
        .duty_resolution  = LEDC_DUTY_RES,
        .freq_hz          = LEDC_FREQUENCY,  // Set output frequency at 5 kHz
        .clk_cfg          = LEDC_AUTO_CLK
    };
    ESP_ERROR_CHECK(ledc_timer_config(&ledc_timer));

    // Prepare and then apply the LEDC PWM channel configuration
    ledc_channel_config_t ledc_channel = {
        .speed_mode     = LEDC_MODE,
        .channel        = LEDC_CHANNEL,
        .timer_sel      = LEDC_TIMER,
        .intr_type      = LEDC_INTR_DISABLE,
        .gpio_num       = LEDC_OUTPUT_IO,
        .duty           = 0, // Set duty to 0%
        .hpoint         = 0
    };
    ESP_ERROR_CHECK(ledc_channel_config(&ledc_channel));
    // gpio_set_direction(LEDC_OUTPUT_IN1,GPIO_MODE_OUTPUT);
    // gpio_set_level(LEDC_OUTPUT_IN1,1);
    // gpio_set_direction(LEDC_OUTPUT_IN2,GPIO_MODE_OUTPUT);
    // gpio_set_level(LEDC_OUTPUT_IN2,0);


}

void motor(int speed)
{
    int LEDC_DUTY = speed;
    // Set the LEDC peripheral configuration
    example_ledc_init();
    // Set duty to 50%
    ESP_ERROR_CHECK(ledc_set_duty(LEDC_MODE, LEDC_CHANNEL, LEDC_DUTY));
    // Update duty to apply the new value
    ESP_ERROR_CHECK(ledc_update_duty(LEDC_MODE, LEDC_CHANNEL));
}
