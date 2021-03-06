Installation
============

To deploy Freelan build tools, run the following command:

> ./setup.py install

Libraries
=========

FreeLAN related libraries are based on several libraries which you have to build first.

Explaining exactly how to compile those libraries should be out of the scope of these tools but since we are nice, here is quick-guide to get started:

Boost
-----

First download Boost from [its official website](http://www.boost.org/) and decompress the archive.

To build the Boost::Python library, you will also require Python.

### Windows 32/64 bits

Open a console to the decompressed Boost directory and type:

> .\bootstrap.bat

To build the build tools.

Then, depending on your target platform:

#### MinGW

`gcc` must be in your PATH for this command to work.

For 32 bits:

> .\b2.exe install toolset=gcc --prefix=C:\Boost

For 64 bits:

> .\b2.exe install toolset=gcc address-model=64 --prefix=C:\Boost

#### Microsoft Visual Studio

You must run this command from a "Visual Studio command prompt" (or a "x64 Visual Studio command prompt" for x64 systems).

For 32 bits:

> .\b2.exe install toolset=msvc --prefix=C:\Boost-VC

For 64 bits:

> .\b2.exe install toolset=msvc address-model=64 --prefix=C:\Boost-VC

This will build and install all Boost static libraries, in both release and debug configurations.

Whatever the target platform, you may of course adapt the `--prefix` to whatever you like.

### Mac OS X

Open a terminal and follow all instructions to compile universal libraries

> ./bootstrap.sh
> sudo ./b2 toolset=darwin threading=multi architecture=combined address-model=32_64 --prefix=/usr/local install

OpenSSL
-------

To build OpenSSL, you need a working [Perl installation](http://www.perl.org/).

Download OpenSSL from [its official website](http://www.openssl.org/) and decompress the archive.

### Windows 32/64 bits

#### MinGW

You must run these commands from a MSys console.

For 32 bits:

> perl Configure mingw no-shared no-asm --prefix=/c/OpenSSL

For 64 bits:

> perl Configure mingw64 no-shared no-asm --prefix=/C/OpenSSL-x64

Then:

> make depend

> make

> make install

The `make depend` line is only needed on the most recent OpenSSL version if you specified any of the `no-...` options.

Note that this will compile OpenSSL in static mode.

If at some point you get a "make (e=2):" error, ensure you don't have another "make.exe" in your PATH or just type `/bin/make` instead of `make`.

#### Microsoft Visual Studio

You must run these commands from a "Visual Studio command prompt".

For 32 bits:

> perl Configure VC-WIN32 no-asm --prefix=C:\OpenSSL-VC

> ms\do_ms

For 64 bits:

> perl Configure VC-WIN64A --prefix=C:\OpenSSL-VC-x64

> ms\do_win64a

Then:

> nmake -f ms\ntdll.mak

> nmake -f ms\ntdll.mak install

To build in shared mode or:

> nmake -f ms\nt.mak

> nmake -f ms\nt.mak install

To build in static mode.

### Mac OS X

Open a terminal and follow all instructions to compile universal libraries

> ./Configure darwin-i386-cc --prefix=/usr/local shared
> make
> make install

> mkdir 32
> cp /usr/local/lib/libssl.* /usr/local/lib/libcrypto.* 32

> make clean && rm *.a *.dylib
> ./Configure darwin64-x86_64-cc --prefix=/usr/local shared
> make
> sudo make install 

> mkdir 64
> cp /usr/local/lib/libssl.* /usr/local/lib/libcrypto.* 64

> lipo -create 32/libcrypto.a 64/libcrypto.a -output libcrypto.a
> lipo -create 32/libssl.a 64/libssl.a -output libssl.a
> lipo -create 32/libcrypto.1.0.0.dylib 64/libcrypto.1.0.0.dylib -output libcrypto.1.0.0.dylib
> lipo -create 32/libssl.1.0.0.dylib 64/libssl.1.0.0.dylib -output libssl.1.0.0.dylib
> sudo mv libcrypto.a libssl.a libcrypto.1.0.0.dylib libssl.1.0.0.dylib /usr/local/lib/

libiconv
--------

To build libiconv, you need a MinGW installation and MSys (even for Microsoft Visual Studio).

Download the latest libiconv source from its [official website](http://www.gnu.org/s/libiconv/) and decompress the archive.

### MinGW

The preferred method is to compile libiconv in a static library.

Fire up a MSYS console, go into the libiconv extracted archive directory and type:

> ./configure --enable-shared=no --enable-static=yes --prefix=/c/iconv

Or for the shared library version:

> ./configure --prefix=/c/iconv

Then, in both cases:

> make

> make install

### Microsoft Visual Studio

libiconv dropped official support for Visual Studio after its 11.1 version. However, there is a way to get a working iconv library for Visual Studio:

Follow the steps to build the **shared** library version with MinGW. Just change the `--prefix` to something else, like `/c/iconv-VC`.

> ./configure --prefix=/c/iconv-VC

> make

> make install

Close MSys, fire up a Visual Studio command prompt and go to installed directory, `C:\iconv-VC`. Type:

> dumpbin /exports bin\libiconv-2.dll

Which will show you the list of exported symbols.

Copy that list to a `lib\iconv.def` file, beginning with `EXPORTS`. You should get a file like:

    EXPORTS
    _libiconv_version
    aliases2_lookup
    aliases_lookup
    iconv_canonicalize
    libiconv
    libiconv_close
    libiconv_open
    libiconv_open_into
    libiconv_relocate
    libiconv_set_relocation_prefix
    libiconvctl
    libiconvlist
    locale_charset

Then, generate the `iconv.lib` file, with the following command:

> lib /def:lib\iconv.def /out:lib\iconv.lib /machine:x86

Or for a x64 version:

> lib /def:lib\iconv.def /out:lib\iconv.lib /machine:x64

libcurl
-------

Download the latest libcurl source from its [official website](http://curl.haxx.se/download.html).

To build libcurl with SSL support (needed for freelan), you must build OpenSSL first.

### MinGW

We assume here that OpenSSL is built and installed in the `C:\OpenSSL` or `C:\OpenSSL-x64` directories.

Extract the archive where you like then go into the extracted folder with a MSys console.

For 32 bits:

> ./configure --disable-shared --enable-static --enable-ipv6 --disable-ldap --disable-ldaps --with-ssl=/c/OpenSSL --prefix=/c/cURL

For 64 bits:

> ./configure --disable-shared --enable-static --enable-ipv6 --disable-ldap --disable-ldaps --with-ssl=/c/OpenSSL-x64 --prefix=/c/cURL-x64

Then, for both architectures:

> make && make install

### Microsoft Visual Studio

We assume here that OpenSSL is built and installed in the `C:\OpenSSL-VC` or `C:\OpenSSL-VC-x64` directories.

Extract the archive where you like then go into the extracted folder with a Windows SDK console.

For 32 bits:

> setenv /xp /x86 /release

> cd winbuild

> nmake -f Makefile.vc mode=static USE_IDN=no VC=10 WITH_DEVEL=C:\OpenSSL-VC\ WITH_IPV6=yes WITH_SSL=dll

> xcopy /S /I ..\builds\libcurl-release-static-ssl-dll-ipv6-sspi C:\cURL-VC

For 64 bits:

> setenv /xp /x64 /release

> cd winbuild

> nmake -f Makefile.vc mode=static USE_IDN=no VC=10 WITH_DEVEL=C:\OpenSSL-VC-x64\ WITH_IPV6=yes WITH_SSL=dll MACHINE=x64

> xcopy /S /I ..\builds\libcurl-release-static-ssl-dll-ipv6-sspi C:\cURL-VC-x64

Change the value of `VC=10` to match your current Visual C++ Compiler version.

*The `MACHINE=x64` should not be needed but I had troubles without it.*

If your OpenSSL version was built statically, replace `WITH_SSL=dll` with `WITH_SSL=static` and update the `xcopy` command accordingly as the output directory name will change too.
