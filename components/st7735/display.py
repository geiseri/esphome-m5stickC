import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import display, spi
from esphome.const import CONF_ID, CONF_LAMBDA, CONF_DC_PIN, CONF_CS_PIN, CONF_MODEL
from esphome.const import CONF_RESET_PIN, CONF_BRIGHTNESS

DEPENDENCIES = ['spi']

st7735_ns = cg.esphome_ns.namespace('st7735')

ST7735 = st7735_ns.class_('ST7735', cg.PollingComponent, spi.SPIDevice, display.DisplayBuffer)
ST7735Ref = ST7735.operator('ref')
ST7735Redtab = st7735_ns.class_('ST7735Redtab', ST7735)
ST7735Greentab = st7735_ns.class_('ST7735Greentab', ST7735)
ST7735Blacktab = st7735_ns.class_('ST7735Blacktab', ST7735)
ST7735Greentab_144 = st7735_ns.class_('ST7735Greentab_144', ST7735)
ST7735Mini_160_80 = st7735_ns.class_('ST7735Mini_160_80', ST7735)
ST7735MStickC = st7735_ns.class_('ST7735M5StickC', ST7735)
  
MODELS = {
    'blacktabex': ST7735,
    'redtab': ST7735Redtab,
    'greentab': ST7735Greentab,
    'blacktab': ST7735Blacktab,
    'greentab_144': ST7735Greentab_144,
    'mini_160_80': ST7735Mini_160_80,
    'm5stickc': ST7735MStickC,
}


CONFIG_SCHEMA = display.FULL_DISPLAY_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(ST7735),
    cv.Required(CONF_MODEL): cv.one_of(*MODELS, lower=True),
    cv.Required(CONF_RESET_PIN): pins.gpio_output_pin_schema,
    cv.Required(CONF_DC_PIN): pins.gpio_output_pin_schema,
    cv.Required(CONF_CS_PIN): pins.gpio_output_pin_schema,
    cv.Optional(CONF_BRIGHTNESS, default=1.0): cv.percentage,
}).extend(cv.polling_component_schema('1s')).extend(spi.spi_device_schema())

def to_code(config):
    model = MODELS[config[CONF_MODEL]]
    rhs = model.new()
    var = cg.Pvariable(config[CONF_ID], rhs, model)
    yield cg.register_component(var, config)
    yield spi.register_spi_device(var, config)

    dc = yield cg.gpio_pin_expression(config[CONF_DC_PIN])
    cg.add(var.set_dc_pin(dc))

    reset = yield cg.gpio_pin_expression(config[CONF_RESET_PIN])
    cg.add(var.set_reset_pin(reset))

    if CONF_LAMBDA in config:
        lambda_ = yield cg.process_lambda(
            config[CONF_LAMBDA], [(display.DisplayBufferRef, 'it')], return_type=cg.void)
        cg.add(var.set_writer(lambda_))

    yield display.register_display(var, config)
