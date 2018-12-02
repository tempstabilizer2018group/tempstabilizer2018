esp-idf-master\components\esp32\sleep_modes.c
=============================================
static uint32_t IRAM_ATTR esp_sleep_start(uint32_t pd_flags)
    uint32_t result = rtc_sleep_start(s_config.wakeup_triggers, 0);

void IRAM_ATTR esp_deep_sleep_start()
  uint32_t pd_flags = get_power_down_flags();
  // Enter sleep
  esp_sleep_start(RTC_SLEEP_PD_DIG | RTC_SLEEP_PD_VDDSDIO | RTC_SLEEP_PD_XTAL | pd_flags);

static esp_err_t esp_light_sleep_inner(uint32_t pd_flags,
  esp_err_t err = esp_sleep_start(pd_flags);

esp_err_t esp_light_sleep_start()
  // Decide which power domains can be powered down
  uint32_t pd_flags = get_power_down_flags();
  pd_flags |= RTC_SLEEP_PD_VDDSDIO;

static uint32_t get_power_down_flags()
  // If there is any data placed into .rtc.data or .rtc.bss segments, and
  // RTC_SLOW_MEM is Auto, keep it powered up as well.
  // Prepare flags based on the selected options
  uint32_t pd_flags = 0;
  pd_flags |= RTC_SLEEP_PD_RTC_FAST_MEM;
  pd_flags |= RTC_SLEEP_PD_RTC_SLOW_MEM;
  pd_flags |= RTC_SLEEP_PD_RTC_PERIPH;
  pd_flags |= RTC_SLEEP_PD_XTAL;
  return pd_flags;


static uint32_t IRAM_ATTR esp_sleep_start(uint32_t pd_flags)

    // Enter sleep
    rtc_sleep_config_t config = RTC_SLEEP_CONFIG_DEFAULT(pd_flags);
    rtc_sleep_init(config);

    uint32_t result = rtc_sleep_start(s_config.wakeup_triggers, 0);

esp-idf-master\components\soc\esp32\include\soc\rtc.h
=====================================================
/**
 * @brief Prepare the chip to enter sleep mode
 *
 * This function configures various power control state machines to handle
 * entry into light sleep or deep sleep mode, switches APB and CPU clock source
 * (usually to XTAL), and sets bias voltages for digital and RTC power domains.
 *
 * This function does not actually enter sleep mode; this is done using
 * rtc_sleep_start function. Software may do some other actions between
 * rtc_sleep_init and rtc_sleep_start, such as set wakeup timer and configure
 * wakeup sources.
 * @param cfg sleep mode configuration
 */
void rtc_sleep_init(rtc_sleep_config_t cfg);

/**
 * @brief Enter deep or light sleep mode
 *
 * This function enters the sleep mode previously configured using rtc_sleep_init
 * function. Before entering sleep, software should configure wake up sources
 * appropriately (set up GPIO wakeup registers, timer wakeup registers,
 * and so on).
 *
 * If deep sleep mode was configured using rtc_sleep_init, and sleep is not
 * rejected by hardware (based on reject_opt flags), this function never returns.
 * When the chip wakes up from deep sleep, CPU is reset and execution starts
 * from ROM bootloader.
 *
 * If light sleep mode was configured using rtc_sleep_init, this function
 * returns on wakeup, or if sleep is rejected by hardware.
 *
 * @param wakeup_opt  bit mask wake up reasons to enable (RTC_xxx_TRIG_EN flags
 *                    combined with OR)
 * @param reject_opt  bit mask of sleep reject reasons:
 *                      - RTC_CNTL_GPIO_REJECT_EN
 *                      - RTC_CNTL_SDIO_REJECT_EN
 *                    These flags are used to prevent entering sleep when e.g.
 *                    an external host is communicating via SDIO slave
 * @return non-zero if sleep was rejected by hardware
 */
uint32_t rtc_sleep_start(uint32_t wakeup_opt, uint32_t reject_opt);

esp-idf-master\components\soc\esp32\rtc_sleep.c
===============================================
void rtc_sleep_init(rtc_sleep_config_t cfg)
  Wichtig könnte sein:
    RTC_CNTL_PWC_REG, RTC_CNTL_PD_EN  Enable power down rtc_peri in sleep. (R/W)
    RTC_CNTL_XTL_FORCE_PU Crystal force power up. (R/W)
    RTC_CNTL_XTL_FORCE_PD Crystal force power down. (R/W)

esp-idf-master\components\driver\rtc_module.c
=============================================
Suche nach: rtc_gpio_init(): This function must be called when initializing a pad for an analog function.

static esp_err_t dac_rtc_pad_init(dac_channel_t channel)
{
    RTC_MODULE_CHECK((channel >= DAC_CHANNEL_1) && (channel < DAC_CHANNEL_MAX), DAC_ERR_STR_CHANNEL_ERROR, ESP_ERR_INVALID_ARG);
    gpio_num_t gpio_num = 0;
    dac_pad_get_io_num(channel, &gpio_num);
    rtc_gpio_init(gpio_num);
    rtc_gpio_output_disable(gpio_num);
    rtc_gpio_input_disable(gpio_num);
    rtc_gpio_pullup_dis(gpio_num);
    rtc_gpio_pulldown_dis(gpio_num);

    return ESP_OK;
}

micropython-master\ports\esp32\machine_dac.c
============================================

STATIC mp_obj_t mdac_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw,
        const mp_obj_t *args) {
    esp_err_t err = dac_output_enable(self->dac_id);
    if (err == ESP_OK) {
        err = dac_output_voltage(self->dac_id, 0);
    }

esp-idf-master\components\driver\rtc_module.c
=============================================
esp_err_t dac_output_enable(dac_channel_t channel)
{
    RTC_MODULE_CHECK((channel >= DAC_CHANNEL_1) && (channel < DAC_CHANNEL_MAX), DAC_ERR_STR_CHANNEL_ERROR, ESP_ERR_INVALID_ARG);
    dac_rtc_pad_init(channel);
    portENTER_CRITICAL(&rtc_spinlock);
    dac_output_set_enable(channel, true);
    portEXIT_CRITICAL(&rtc_spinlock);

    return ESP_OK;
}

static esp_err_t dac_rtc_pad_init(dac_channel_t channel)
{
    RTC_MODULE_CHECK((channel >= DAC_CHANNEL_1) && (channel < DAC_CHANNEL_MAX), DAC_ERR_STR_CHANNEL_ERROR, ESP_ERR_INVALID_ARG);
    gpio_num_t gpio_num = 0;
    dac_pad_get_io_num(channel, &gpio_num);
    rtc_gpio_init(gpio_num);
    rtc_gpio_output_disable(gpio_num);
    rtc_gpio_input_disable(gpio_num);
    rtc_gpio_pullup_dis(gpio_num);
    rtc_gpio_pulldown_dis(gpio_num);

    return ESP_OK;
}

=================
SENS_DAC_INV