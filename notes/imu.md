---
title: IMU
section: Electronique
tags: [imu, capteurs]
---

# IMU


```python
# -------------------------
# Startup
# -------------------------
@app.on_event("startup")
def startup():
    global PAGES

    # Chargement initial des pages
    PAGES = load_pages()

    # Watcher markdown
    Thread(
        target=start_watcher,
        args=(PAGES,),
        daemon=True
    ).start()

    # Watcher config.yml
    Thread(
        target=start_config_watcher,
        daemon=True
    ).start()
```
## First
### test1
```python
# -------------------------
# Startup
# -------------------------
@app.on_event("startup")
def startup():
    global PAGES

    # Chargement initial des pages
    PAGES = load_pages()

    # Watcher markdown
    Thread(
        target=start_watcher,
        args=(PAGES,),
        daemon=True
    ).start()

    # Watcher config.yml
    Thread(
        target=start_config_watcher,
        daemon=True
    ).start()
```

## Second
### test2
```python
# -------------------------
# Startup
# -------------------------
@app.on_event("startup")
def startup():
    global PAGES

    # Chargement initial des pages
    PAGES = load_pages()

    # Watcher markdown
    Thread(
        target=start_watcher,
        args=(PAGES,),
        daemon=True
    ).start()

    # Watcher config.yml
    Thread(
        target=start_config_watcher,
        daemon=True
    ).start()
```