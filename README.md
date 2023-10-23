# NuzLocke v0.1.1
This is an interactive python based tool to manage your Nuzlocke runs and pokemon.
To run NuzLocke via Terminal:


```
python NuzLocke.py
```

An optional argument can be given to specify your used edition:

```
python NuzLocke.py -edition OmegaRuby
```


## Latest changes with v0.1.1:
 - Implemented possibility to manually change an attribute of a Pokemon
    - All attributes (except id) can now manually be adjusted in case of some mistake before
    - status can only be changed to "Team", "boxed", "dead", and "failed"
      - if status is set to "failed", the species and the nickname will be deleted

      
### Required Libraries:
 - python
 - numpy
 - hjson

### Upcoming Features:
 - ending a Run to save some statistics into a file
 - tracking of run number




