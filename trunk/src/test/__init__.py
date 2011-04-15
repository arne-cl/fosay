# -*- coding: utf-8 -*-
import unittest
import test.core.test_constants as test_constants
import test.core.lang.test_process as test_process
import test.core.lang.test_translate as test_translate
import test.core.compilers.test_gener_tools as test_gener_tools
import test.core.models.test_lang as test_lang
import test.core.compilers.test_atnl as test_atnl
import test.core.compilers.test_cws as test_cws

#ts = [test.core.pythologic.test_funcs.suite]
#all_suites = unittest.TestSuite(ts)
#unittest.TextTestRunner(verbosity=2).run(all_suites)

ts = [unittest.TestLoader().loadTestsFromModule(test_constants)]
ts += [unittest.TestLoader().loadTestsFromModule(test_gener_tools)]
#ts += [unittest.TestLoader().loadTestsFromModule(test_process)]
ts += [unittest.TestLoader().loadTestsFromModule(test_atnl)]
ts += [unittest.TestLoader().loadTestsFromModule(test_cws)]
#ts += [unittest.TestLoader().loadTestsFromModule(test_lang)]
ts += [unittest.TestLoader().loadTestsFromModule(test_translate)]
t = unittest.TestSuite(ts)
unittest.TextTestRunner(verbosity=2).run(t)