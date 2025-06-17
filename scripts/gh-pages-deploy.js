/*
 * Script from https://blog.logrocket.com/automatically-build-deploy-vuejs-app-github-pages/ who credited https://dev.to/the_one/deploy-to-github-pages-like-a-pro-with-github-actions-4hdg
 */

/* eslint-disable no-console */
import { execa } from "execa";
import fs from "fs";

(async () => {
  try {
    await execa('git', ['checkout', '--orphan', 'gh-pages']);
    console.log('Building started...');
    await execa('npm', ['run', 'build']);

    // Determine if it's dist or build folder
    const folderName = fs.existsSync('dist') ? 'dist' : 'build';

    await execa('git', ['--work-tree', folderName, 'add', '--all']);
    await execa('git', ['--work-tree', folderName, 'commit', '-m', 'gh-pages']);
    console.log('Pushing to gh-pages...');
    await execa('git', ['push', 'origin', 'HEAD:gh-pages', '--force']);

    // Check the operating system to use the correct command for removing the directory
    if (process.platform === 'win32') {
      // Windows command to remove directory
      await execa('cmd', ['/C', 'rd', '/s', '/q', folderName]);
    } else {
      // Unix-like command to remove directory
      await execa('rm', ['-r', folderName]);
    }

    await execa('git', ['checkout', '-f', 'master']);
    await execa('git', ['branch', '-D', 'gh-pages']);
    console.log('Successfully deployed, check your settings');
  } catch (e) {
    console.log(e.message);
    process.exit(1);
  }
})();
