import { execa } from "execa";
import fs from "fs";

const python_executable = 'python'; // Command to use python

(async () => {
  try {
    console.log('Running export_databases.py...');
    await execa('python', ['../dea_db/export_databases.py'], {
      env: {
        ...process.env,
        PYTHONUTF8: '1',
        PYTHONIOENCODING: 'utf-8',
      },
      stdio: 'inherit',
    });
    
    console.log('Databases successfully exported !');
  } catch (e) {
    console.log(e.message);
    process.exit(1);
  }
})();
