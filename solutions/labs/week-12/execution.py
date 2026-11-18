def run_fixed_tests(executor,cwd,python_executable):
    if not isinstance(python_executable,str) or not python_executable:
        raise ValueError("interpreter path required")
    return executor.run((python_executable,"-m","unittest","discover","-s","tests"),
        cwd=cwd,timeout=30)
