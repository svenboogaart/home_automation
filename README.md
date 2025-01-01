[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

# Home Automation

Using lights and sensors for custom automations.
Hue based easy to extend for different platfroms.

Some options

- Send an e-mail if motions is detected
- Options to activate home security by using the hue switch.
- Flash your lights in any color if motions is detected
- Play alarm sound if motions is detected

## Requirements

Python 3.9+

## Lights

Based on philips hue:
https://developers.meethue.com/develop/get-started-2/

## Supported Device and Event Types

| Device            | Event-Type (eventType) | Event-Data (triggerOn) | Description                                                |
|-------------------|------------------------|------------------------|------------------------------------------------------------|
| Hue Tap           | buttonevent            | 34                     | 1 Dot Key                                                  |
|                   | buttonevent            | 16                     | 2 Dot Key                                                  |
|                   | buttonevent            | 17                     | 3 Dot Key                                                  |
|                   | buttonevent            | 18                     | 4 Dot Key                                                  |
| Hue Dimmer Switch | buttonevent            | 1000                   | Hard press ON, followed by Event-Data 1002                 |
|                   | buttonevent            | 1001                   | Long press ON (send while hold the button)                 |
|                   | buttonevent            | 1003                   | Release ON (after Long press)                              |
|                   | buttonevent            | 1002                   | Soft press ON                                              |
|                   | buttonevent            | 2000                   | Hard press BRIGHTER, followed by Event-Data 2002           |
|                   | buttonevent            | 2001                   | Long press BRIGHTER (send while hold the button)           |
|                   | buttonevent            | 2003                   | Release BRIGHTER                                           |
|                   | buttonevent            | 2002                   | Soft press BRIGHTER                                        |
|                   | buttonevent            | 3000                   | Hard press DARKER, followed by Event-Data 3002             |
|                   | buttonevent            | 3001                   | Long press DARKER                                          |
|                   | buttonevent            | 3003                   | Release DARKER                                             |
|                   | buttonevent            | 3002                   | Soft press DARKER                                          |
|                   | buttonevent            | 4000                   | Hard press OFF, followed by Event-Data 4002                |
|                   | buttonevent            | 4001                   | Long press OFF                                             |
|                   | buttonevent            | 4003                   | Release OFF                                                |
|                   | buttonevent            | 4002                   | Soft press OFF                                             |
| Hue Motion Sensor | presence               | true                   | Motion detected                                            |
|                   | presence               | false                  | No Motion detected                                         |
|                   | temperature            | xxxx                   | Temperature in °C multiplied by 100 (2655 == 26.55°C)      |
|                   | lightlevel             | xxxxx                  | Lightlevel (0 ~ dark, 20000 ~ normal, 40000 ~ very bright) |

## Hue light types

| **Type**                    | **Capabilities**                                      | **Examples**                                         |
|-----------------------------|-------------------------------------------------------|------------------------------------------------------|
| **Extended Color Light**    | Full RGB color control, brightness, color temperature | Hue White and Color Ambiance, Hue Lightstrip Plus    |
| **Color Temperature Light** | Adjust white temperature (warm to cool white)         | Hue White Ambiance                                   |
| **Dimmable Light**          | Dimming only, fixed white color                       | Hue White bulbs                                      |
| **Effect Light**            | Dynamic lighting effects (e.g., colorloop)            | Hue Lightstrips, Hue Play                            |
| **White Light**             | Fixed white, dimming only                             | Hue White bulbs                                      |
| **Lightstrip**              | Full RGB color control, effects, brightness           | Hue Lightstrip Plus, Hue Play                        |
| **Lamps & Fixtures**        | White or RGB light, color temperature control         | Hue Go, Hue Play, Hue White and Color Ambiance lamps |
| **Group Light**             | Control multiple lights together                      | Group of Hue bulbs in a room                         |
