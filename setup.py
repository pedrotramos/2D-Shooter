import cx_Freeze

executables = [cx_Freeze.Executable('Código.py')]

cx_Freeze.setup(
        name = 'GOTU',
        options = {'build_exe':{'packages':['pygame'],
                                'include_files':['Assets',
                                                 'snd',
                                                 'highscore.txt']}},
        description = 'Guardians Of The Universe',
        executables = executables
        
        )

