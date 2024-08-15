import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation
from esphome.const import (
    CONF_ID,
    CONF_TRIGGER_ID,
)
from esphome.components import uart

DEPENDENCIES = ["uart"]
CODEOWNERS = ["@sonblack"]
MULTI_CONF = True

sim7680c_ns = cg.esphome_ns.namespace("sim7680c")
Sim7680cComponent = sim7680c_ns.class_("Sim7680cComponent", cg.Component)

Sim7680cReceivedMessageTrigger = sim7680c_ns.class_(
    "Sim7680cReceivedMessageTrigger",
    automation.Trigger.template(cg.std_string, cg.std_string),
)
Sim7680cIncomingCallTrigger = sim7680c_ns.class_(
    "Sim7680cIncomingCallTrigger",
    automation.Trigger.template(cg.std_string),
)
Sim7680cCallConnectedTrigger = sim7680c_ns.class_(
    "Sim7680cCallConnectedTrigger",
    automation.Trigger.template(),
)
Sim7680cCallDisconnectedTrigger = sim7680c_ns.class_(
    "Sim7680cCallDisconnectedTrigger",
    automation.Trigger.template(),
)

Sim7680cReceivedUssdTrigger = sim7680c_ns.class_(
    "Sim7680cReceivedUssdTrigger",
    automation.Trigger.template(cg.std_string),
)

# Actions
Sim7680cSendSmsAction = sim7680c_ns.class_("Sim7680cSendSmsAction", automation.Action)
Sim7680cSendUssdAction = sim7680c_ns.class_("Sim7680cSendUssdAction", automation.Action)
Sim7680cDialAction = sim7680c_ns.class_("Sim7680cDialAction", automation.Action)
Sim7680cConnectAction = sim7680c_ns.class_("Sim7680cConnectAction", automation.Action)
Sim7680cDisconnectAction = sim7680c_ns.class_(
    "Sim7680cDisconnectAction", automation.Action
)

CONF_SIM7680C_ID = "sim7680c_id"
CONF_ON_SMS_RECEIVED = "on_sms_received"
CONF_ON_USSD_RECEIVED = "on_ussd_received"
CONF_ON_INCOMING_CALL = "on_incoming_call"
CONF_ON_CALL_CONNECTED = "on_call_connected"
CONF_ON_CALL_DISCONNECTED = "on_call_disconnected"
CONF_RECIPIENT = "recipient"
CONF_MESSAGE = "message"
CONF_USSD = "ussd"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(Sim7680cComponent),
            cv.Optional(CONF_ON_SMS_RECEIVED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        Sim7680cReceivedMessageTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_INCOMING_CALL): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        Sim7680cIncomingCallTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_CALL_CONNECTED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        Sim7680cCallConnectedTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_CALL_DISCONNECTED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        Sim7680cCallDisconnectedTrigger
                    ),
                }
            ),
            cv.Optional(CONF_ON_USSD_RECEIVED): automation.validate_automation(
                {
                    cv.GenerateID(CONF_TRIGGER_ID): cv.declare_id(
                        Sim7680cReceivedUssdTrigger
                    ),
                }
            ),
        }
    )
    .extend(cv.polling_component_schema("5s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)
FINAL_VALIDATE_SCHEMA = uart.final_validate_device_schema(
    "sim7680c", require_tx=True, require_rx=True
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)

    for conf in config.get(CONF_ON_SMS_RECEIVED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(
            trigger, [(cg.std_string, "message"), (cg.std_string, "sender")], conf
        )
    for conf in config.get(CONF_ON_INCOMING_CALL, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(cg.std_string, "caller_id")], conf)
    for conf in config.get(CONF_ON_CALL_CONNECTED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)
    for conf in config.get(CONF_ON_CALL_DISCONNECTED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [], conf)

    for conf in config.get(CONF_ON_USSD_RECEIVED, []):
        trigger = cg.new_Pvariable(conf[CONF_TRIGGER_ID], var)
        await automation.build_automation(trigger, [(cg.std_string, "ussd")], conf)


SIM7680C_SEND_SMS_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(Sim7680cComponent),
        cv.Required(CONF_RECIPIENT): cv.templatable(cv.string_strict),
        cv.Required(CONF_MESSAGE): cv.templatable(cv.string),
    }
)


@automation.register_action(
    "sim7680c.send_sms", Sim7680cSendSmsAction, SIM7680C_SEND_SMS_SCHEMA
)
async def sim7680c_send_sms_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_RECIPIENT], args, cg.std_string)
    cg.add(var.set_recipient(template_))
    template_ = await cg.templatable(config[CONF_MESSAGE], args, cg.std_string)
    cg.add(var.set_message(template_))
    return var


SIM7680C_DIAL_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(Sim7680cComponent),
        cv.Required(CONF_RECIPIENT): cv.templatable(cv.string_strict),
    }
)


@automation.register_action("sim7680c.dial", Sim7680cDialAction, SIM7680C_DIAL_SCHEMA)
async def sim7680c_dial_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_RECIPIENT], args, cg.std_string)
    cg.add(var.set_recipient(template_))
    return var


@automation.register_action(
    "sim7680c.connect",
    Sim7680cConnectAction,
    cv.Schema({cv.GenerateID(): cv.use_id(Sim7680cComponent)}),
)
async def sim7680c_connect_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    return var


SIM7680C_SEND_USSD_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.use_id(Sim7680cComponent),
        cv.Required(CONF_USSD): cv.templatable(cv.string_strict),
    }
)


@automation.register_action(
    "sim7680c.send_ussd", Sim7680cSendUssdAction, SIM7680C_SEND_USSD_SCHEMA
)
async def sim7680c_send_ussd_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    template_ = await cg.templatable(config[CONF_USSD], args, cg.std_string)
    cg.add(var.set_ussd(template_))
    return var


@automation.register_action(
    "sim7680c.disconnect",
    Sim7680cDisconnectAction,
    cv.Schema({cv.GenerateID(): cv.use_id(Sim7680cComponent)}),
)
async def sim7680c_disconnect_to_code(config, action_id, template_arg, args):
    paren = await cg.get_variable(config[CONF_ID])
    var = cg.new_Pvariable(action_id, template_arg, paren)
    return var
