##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class Podio(CMakePackage):
    """PODIO, or plain-old-data I/O, is a C++ library to support the creation
    and handling of data models in particle physics."""

    homepage = "https://github.com/AIDASOFT/podio"
    url      = "https://github.com/AIDASoft/podio/archive/v00-09-02.tar.gz"

    version('00-09-02', sha256='8234d1b9636029124235ef81199a1220968dcc7fdaeab81cdc96a47af332d240',  extension='tar.gz', preferred=True)
    version('00-09', sha256='3cde67556b6b76fd2d004adfaa3b3b6173a110c0c209792bfdb5f9353e21076f')
    version('00-08', sha256='9d035a7f5ebfae5279a17405003206853271af692f762e2bac8e73825f2af327')
    version('develop', git='https://github.com/AIDASOFT/podio.git', branch='master')

    variant('build_type', default='Release',
            description='The build type to build',
            values=('Debug', 'Release'))

    variant('cxxstd',
            default='17',
            values=('14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('cmake')
    depends_on('root@6.08.06:')
    depends_on('python@2.7:')
    depends_on('py-pyyaml')
    depends_on('tbb')
    depends_on('davix', when='@:00-09')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s' % self.spec.variants['cxxstd'].value)
        args.append('-DBUILD_TESTING=OFF')
        return args

    # in LCG_96 ROOT is installed with an external xz rather than the builtin,
    # so the genreflex binary needs to find it.
    # As root is installed as an external package we cannot modify its
    # setup_dependent_environment function to add the xz lib folder to the
    # LD_LIBRARY_PATH hence we need to do it here.
    depends_on('xz', when='^root@6.16:')

    def setup_environment(self, spack_env, run_env):
        if 'xz' in self.spec:
            spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['xz'].prefix.lib)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('PODIO', self.prefix)

    def setup_build_environment(self, build_env):
      build_env.prepend_path('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)
      if 'xz' in self.spec:
         build_env.prepend_path('LD_LIBRARY_PATH', self.spec['xz'].prefix.lib)

    def setup_run_environment(self, run_env):
      run_env.prepend_path('LD_LIBRARY_PATH', self.spec['root'].prefix.lib)
      if 'xz' in self.spec:
         spack_env.prepend_path('LD_LIBRARY_PATH', self.spec['xz'].prefix.lib)
