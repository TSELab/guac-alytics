# GUAC-ALYTICS

## Table of Contents

- [GUAC-ALYTICS](#GUAC-ALYTICS)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [How To Install](#how-to-install)
    - [From Source](#from-source)
  - [How to Run](#how-to-run)
    - [As Individual Scripts](#as-individual-scripts)
  - [Data Representation](#data-representation)
  - [Other Information](#other-information)


## About

Guac-alytics is a collection of tools and resources designed to help researchers and practitioners better understand the risk profile of open-source software ecosystems. 
The repository contains scripts for collecting, initializing, and handling various datasets required for analyzing open-source software ecosystems. 

More information about the project can be found on its [website](https://rcodi.org/project/guac-alytics/).

## How To Install

Before running this project, you need to package and install it.

The package can be installed from our [From Source](#from-source).

### From Source

> The instructions provided below are for Linux operating systems:

1. Clone the project locally:
   `git clone https://github.com/TSELab/guac-alytics.git`
1. `cd` into the project: `cd guac-alytics`
1. Create a `Python 3` virtual environment: `python3 -m venv env`
1. Activate virtual environment: `source env/bin/activate`


## How to Run

After installing the package/project [from source](#how-to-install), the project can be run as individual scripts.

### As Individual Scripts

To import variables correctly, you need to set up the path inside each script. The repository contains the following directories:
- [scripts](scripts/) directory contains code to help set up the repository (e.g., collect data, initialize the database, etc).
- [ingestion](ingestion/) directory contains functions and scripts to handle a particular data type (e.g., .buildinfo, or pocon data)
- [analytics](analytics) directory contains scripts/models to gather or visualize results based on the information collected.

To run any of the scripts, execute the following command pattern:

- `python 'Scripts Directory'/'Script Name'`

For example
- `python scripts/ingestion/buildinfo_main.py`


## Data Representation

The schema of our data is as follows:

**source_table:**

| source_id (Integer) \<PK> | source_name (varchar)   | version (varchar)    | location (varchar) | 
|--------|---------|--------|--------|
1|maxima|5.42.0-1|

**buildinfo_table:**
| buildinfo_id (Integer) \<PK> | source_id (Integer) \<FK> | type (varchar) | build_origin (varchar) | build_architecture (varchar)    |  build_date (datetime) | build_path (varchar) | environment (varchar)|
|--------|---------|--------|--------|---------|--------|--------|------|
| 1|1|mips|Debian|mips|2018-10-05T02:46:09+00:00|/build/maxima-ffBduW/maxima-5.42.0|  DEB_BUILD_OPTIONS="parallel=2"  LC_ALL="POSIX"  SOURCE_DATE_EPOCH="1538247291" |

**binary_table:**
| binary_id (Integer) \<PK>   | package (varchar) | version (varchar)    | architecture (varchar) |
|--------|---------|--------|--------|
| 1|maxima|5.42.0-1|mips| 

**dependency_table:**
| buildinfo_id (Integer) \<FK>   | build_id (Integer) \<FK>    | 
|--------|---------|
| 1|23|

**output_table:**
|  buildinfo_id (Integer) \<FK>   | build_id (Integer) \<FK>  | checksum_md5 (varchar) | checksum_sha1 (varchar) |checksum_sha256 (varchar)|
|--------|---------|--------|--------|------|
| 1|1|['c671904988b053efb0e49405ad82511e 5736524 maxima_5.42.0-1_mips.deb', '6477b5fca4f2bfc6d09aae67f1efc9ca 485988 xmaxima_5.42.0-1_mips.deb']|['50a417d7b6642250947730b23f173b08e00425dc 5736524 maxima_5.42.0-1_mips.deb', 'f8caa8d98ecfed3717738e0f4ada053b3683e7a5 485988 xmaxima_5.42.0-1_mips.deb']|['d67b0a3b43f8c8cad5ff9b4e4c0120ad7c50021762d9a20560ed785ea0ab2eef 5736524 maxima_5.42.0-1_mips.deb', 'e065f3f443cecc14df0cc55a1df4be547f073dc5422a159cf9d69f97f04ef01d 485988 xmaxima_5.42.0-1_mips.deb']|
 
**popularity_table:** 

| name (text)  | date  (date)  | inst (integer)  | vote (integer)  | old (integer) | recent (integer) | no-files (integer) | maintainer (text) | inst_norm (varchar) | vote_norm  (varchar)|
|--------|---------|--------|--------|------|--------|----------|------------------------------|------------|------------|
| dpkg|02/09/2023|209081|192500|2847|13700|34|Dpkg Developers|195484.300615492|179981.575889164|


**maintainer:**
| name (text)  | package (varchar)  | inst (integer)  | vote (integer)  | old (integer) | recent (integer) | no-files (integer) | 
|--------|---------|--------|--------|------|--------|----------|
| Debian Gnome Maintainers|libvaladoc-0.56-dev | 25913899|8685994|8352785|2749012|6126108|

**publish_packages:**
| Package_id |   Package   | Architecture |      Version       | Section  |  Size  |                         pool_endpoint                          | DFSG |     Added_at     |              MD5sum              |                   SHA1                   |                              SHA256                              | Provided_by |
|------------|-------------|--------------|--------------------|----------|--------|----------------------------------------------------------------|------|------------------|----------------------------------|------------------------------------------|------------------------------------------------------------------|-------------|
| 18221      | imagemagick | amd64        | 8:6.8.9.9-5+deb8u4 | graphics | 156996 | pool/main/i/imagemagick/imagemagick_6.8.9.9-5+deb8u4_amd64.deb | main | 20161231T000000Z | c2cedf60dbc3d6f794fe78fb6d5fbe10 | 82eaef39fe894cf7ca829f3080c445d7e59d4285 | 54ca108d2b61a50dfeaaef1ff3315e52bdd47bb1da1f731c02f2c4b7baf19992 |             |

**publish_dependencies:**
| Dependency_id | Package_id | Dependency_package_id |          Condition          |
|---------------|------------|-----------------------|-----------------------------|
| 5             | 1          | 2359                  | libboost-filesystem1.55.0   |



The data is represented using an ER diagram, which can be edited [here](https://lucid.app/lucidchart/78e7ef88-3d4d-45de-8b48-703ac1b3007a/edit?viewport_loc=-2%2C-9%2C2444%2C1159%2C0_0&invitationId=inv_5f98e40f-8227-4f62-8064-fb249b491d2b).

![ER_diagram](https://user-images.githubusercontent.com/71808684/226646097-15079b0f-2821-4378-a5ac-4468caa162a0.png)

## Other information

See these [slides](https://docs.google.com/presentation/d/1FKthyyVpaDAtYtiiHWIv-lM3RIYWilLE-Bn8NZQ6vEY/edit) to aid contextualize the project. This project may or may not eventually be an overlay over the guacsec code [see](https://github.com/guacsec/guac).

Meeting agenda and notes on [this hackmd](https://hackmd.io/KV42bSFTS5iq1wAfkTX-ow).
