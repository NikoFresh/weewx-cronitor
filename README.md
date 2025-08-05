# weewx-healthchecks

A WeeWX extension that uses [Cronitor.io](https://cronitor.io) to monitor WeeWX.

Every WeeWX report cycle, a success signal is sent to Cronitor.io.

The method(s) of notification are also [selected](https://cronitor.io/docs/heartbeat-monitoring#alert-configuration) at [Cronitor.io](https://cronitor.io).

The [getting started](https://cronitor.io/docs) is a good introduction.

You can add a [status page](https://cronitor.io/docs/status-pages) to display the current state of the system to your visitators.

## Installation
Run `weectl extension install https://github.com/NikoFresh/weewx-cronitor/archive/master.zip`

## Configuration

After installing `weewx-cronitor`, edit `weewx.conf`:

```text
[StdReport]
    [[Cronitor]]
        # Turn the service on and off.
        enable = false
        
        skin = cronitor
        
        # The host to 'ping'
        # Default is cronitor.link/p
        # host = cronitor.link/p 

        # The name for the tracker
        # Default is Weewx
        # device_name = Weewx
        
        # The http request timeout
        # The default is 10
        # timeout = 10
        
        # The Cronitor api_key
        api_key = REPLACE_ME
```

1. Set `enable = true`
2. Set `api_key` to the `api_key` that is associated with the `Heartbeats` of your account at Cronitor.io.

Restart WeeWX

## Example
You can check my [status page](https://meteocentrocadore.cronitorstatus.com/) to see how the data is displayed.

## Credits
Thanks to bellrichm for the original weewx-healthchecks
