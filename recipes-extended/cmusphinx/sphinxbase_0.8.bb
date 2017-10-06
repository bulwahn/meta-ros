DESCRIPTION = "This package contains the basic libraries shared by the CMU Sphinx \
trainer and all the Sphinx decoders (Sphinx-II, Sphinx-III, and \
PocketSphinx), as well as some common utilities for manipulating \
acoustic feature and audio files."
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://COPYING;md5=c550e8ca1106e5eeaf4e2b4cbf960fcf"

SRC_URI[md5sum] = "cb530d737c8f2d1023797cf0587b4e05"
SRC_URI[sha256sum] = "7a07d3f7cca5c0b38ca811984ef8da536da32932d68c1a6cce33ec2462b930bf"

require cmusphinx.inc

SRC_URI += "file://0001-TESTS-srcdir-remove.patch"

do_install_append () {
    #remove egg-info
    rm -rf ${D}/${PYTHON_SITEPACKAGES_DIR}/*.egg-info
}

FILES_${PN} += "${PYTHON_SITEPACKAGES_DIR}/sphinxbase.so"
FILES_${PN}-dbg += "${PYTHON_SITEPACKAGES_DIR}/.debug/*"
