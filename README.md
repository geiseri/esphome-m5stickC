Extending esphome-m5stickc by airy/geiseri base to support more displays.
Hampered by lack of displays for testing.
The .yaml config now includes a  `model: redtab,greentab,blacktab, ...`. 

Only `blacktabex` is tested. The other have `setup()` sequences derived from the Ur display code (Adafruit) or
the projects this was forked from.

To quote:

Mostly a work in progress.  
Copy the components to a `custom_components` directory next to your .yaml configuration file.

- axp192 : power management - configuration hard coded for the M5StickC - should be made more generic.
  Must be present to initialize the screen power.  
  Can be also used to read some of the power info - most sensors aren't published yet.  
  Mostly the AXP192 from M5Stack sample code adapted for esphome.
- st7735 : TFT screen  - configuration hard coded for the M5StickC - should be made more generic.  
  Adapted from https://github.com/musk95/esphome-1/tree/dev/esphome/components/st7789v + M5StickC sample code for the init
