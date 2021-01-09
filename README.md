# Chicken Coop

Schema in schema.xml (how to preview here ?)

## API

For the moment status, but why not automatic things, and as a standalone elements, alerts, etc.

Currently collected to influxdb and monitored with grafana (with weather metrics, etc)

`curl http://chicken-coop`

```
{
    temperature: 7.1,
    humidity: 92,
    outside: {
        temperature: 6.4,
        humidity: 99
    },
    humanDoorStatus: 'CLOSED' # Can be OPEN
}
```
