"""A base environment class."""

import os
import platform

from SCons.Script.SConscript import SConsEnvironment

class BaseEnvironment(SConsEnvironment):
    """A base environment class."""

    def __init__(
        self,
        _platform=None,
        _tools=None,
        toolpath=None,
        variables=None,
        parse_flags=None,
        **kw
    ):
        """Create a new BaseEnvironment instance."""

        if _tools is None:
            toolset = kw.setdefault('ARGUMENTS', {}).get('toolset', os.environ.get('FREELAN_TOOLSET', 'default'))
            _tools = [toolset, 'astyle', 'doxygen', 'nsis', 'innosetup']

        if toolpath is None:
            toolpath = [os.path.abspath(os.path.dirname(__file__))]

        self.arch = kw.setdefault('ARGUMENTS', {}).get('arch', os.environ.get('FREELAN_ARCH', platform.machine()))

        kw.setdefault('TARGET_ARCH', self.arch)

        SConsEnvironment.__init__(
            self,
            _platform,
            _tools,
            toolpath,
            variables,
            parse_flags,
            **kw
        )

        self.mode = kw.setdefault('ARGUMENTS', {}).get('mode', os.environ.get('FREELAN_MODE', 'release'))
        self.bindir = kw.setdefault('ARGUMENTS', {}).get('bindir', os.environ.get('FREELAN_BINDIR', 'bin'))
        self.libdir = kw.setdefault('ARGUMENTS', {}).get('libdir', os.environ.get('FREELAN_LIBDIR', 'lib'))
        self.static_suffix = kw.setdefault('ARGUMENTS', {}).get('static_suffix', os.environ.get('FREELAN_STATIC_SUFFIX', '_static'))

        if not self.mode in ['release', 'debug']:
            raise ValueError('\"mode\" can be either \"release\" or \"debug\"')

        # Parse environment overloads
        if 'ENV' in kw:
            for key, value in kw['ENV'].items():
                if key.startswith('FREELAN_ENV_'):
                    self[key[len('FREELAN_ENV_'):]] = value

        if not 'CXXFLAGS' in self:
            self['CXXFLAGS'] = []
            # begin openwrt, ugly hardcoded patch due to the fact exported linux env variableS  cannot be converted into python arrays
            # => FREELAN_ENV_CXXFLAGS="-I/home/log/openwrt/trunk/staging_dir/target-mips_r2_uClibc-0.9.33.2/usr/include -I/home/log/openwrt/freelan/freelan-all/libcryptoplus/include ..."
            self['CXXFLAGS'] = ["-I/home/log/openwrt/trunk/staging_dir/target-mips_r2_eglibc-2.13/usr/include","-I/home/log/openwrt/freelan/freelan-all/libcryptoplus/include","-I/home/log/openwrt/trunk/build_dir/target-mips_r2_eglibc-2.13/libiconv/include","-I/home/log/openwrt/freelan/freelan-all/libfscp/include","-I/home/log/openwrt/freelan/freelan-all/libasiotap/include","-I/home/log/openwrt/freelan/freelan-all/libfreelan/include"]
            # end openwrt

        if not 'LINKFLAGS' in self:
            self['LINKFLAGS'] = []
            
            # begin openwrt, same ugly patch for linked libs
            self['LINKFLAGS'] = ["-L/home/log/openwrt/trunk/staging_dir/target-mips_r2_eglibc-2.13/usr/lib","-L/home/log/openwrt/freelan/freelan-all/libcryptoplus/lib","-L/home/log/openwrt/trunk/build_dir/target-mips_r2_eglibc-2.13/libiconv","-L/home/log/openwrt/freelan/freelan-all/libfscp/lib","-L/home/log/openwrt/freelan/freelan-all/libasiotap/lib","-L/home/log/openwrt/freelan/freelan-all/libfreelan/lib"]
            # end openwrt            

        if not 'SHLINKFLAGS' in self:
            self['SHLINKFLAGS'] = []

    def FreelanProject(self, project):
        """Build a FreeLAN project."""

        return project.configure_environment(self)

    def FreelanProjectInstall(self, project):
        """Install a FreeLAN project."""

        return project.configure_install_environment(self)

    def FreelanProjectDocumentation(self, project):
        """Generate a Freelan project's documentation."""

        return project.configure_documentation_environment(self)

    def FreelanProjectIndent(self, project):
        """Indent a project source files."""

        return self.Indent(project.files)

    def Indent(self, files):
        """Indent source files."""

        indentation = self.AStyle(files)

        self.AlwaysBuild(indentation)

        return indentation
