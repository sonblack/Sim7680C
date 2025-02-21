import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ENTITY_CATEGORY_DIAGNOSTIC,
    STATE_CLASS_MEASUREMENT,
    UNIT_DECIBEL_MILLIWATT,
)
from . import CONF_SIM7680C_ID, Sim7680CComponent

DEPENDENCIES = ["sim7680c"]

CONF_RSSI = "rssi"

CONFIG_SCHEMA = {
    cv.GenerateID(CONF_SIM7680C_ID): cv.use_id(Sim7680CComponent),
    cv.Optional(CONF_RSSI): sensor.sensor_schema(
        unit_of_measurement=UNIT_DECIBEL_MILLIWATT,
        accuracy_decimals=0,
        device_class=DEVICE_CLASS_SIGNAL_STRENGTH,
        state_class=STATE_CLASS_MEASUREMENT,
        entity_category=ENTITY_CATEGORY_DIAGNOSTIC,
    ),
}


async def to_code(config):
    sim7680c_component = await cg.get_variable(config[CONF_SIM7680C_ID])

    if CONF_RSSI in config:
        sens = await sensor.new_sensor(config[CONF_RSSI])
        cg.add(sim7680c_component.set_rssi_sensor(sens))
