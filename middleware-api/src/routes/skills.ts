// skillsMiddleware.ts

import { spawn } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';

interface SkillVerificationRequest {
  candidateId: string;
  resumeFile?: Buffer; // Remove File type since it's not available in Node.js
  githubUsername?: string;
  kaggleUrls?: string[];
}

interface SkillVerificationResult {
  id: string;
  generated_at: string;
  skills: Array<{
    id: string;
    skill: string;
    confidence: number;
    evidence: string[];
    llm_explain: string;
  }>;
}

// Helper function to safely get error message
function getErrorMessage(error: unknown): string {
  if (error instanceof Error) return error.message;
  return String(error);
}

// Simplified middleware that focuses on skill verification without ZK components for now
export async function initSkillsMiddleware() {
  // Path to the SkillVerification Python script
  const skillVerificationPath = path.join(__dirname, '../../../AI-ZK-Agents');

  async function verifySkills(request: SkillVerificationRequest): Promise<SkillVerificationResult> {
    const tempDir = path.join(__dirname, '../temp');
    await fs.mkdir(tempDir, { recursive: true });

    const args = ['scripts/test_skill_verification.py', '--candidate-id', request.candidateId];
    
    // Handle resume file
    if (request.resumeFile) {
      const resumePath = path.join(tempDir, `${request.candidateId}-resume.pdf`);
      await fs.writeFile(resumePath, request.resumeFile);
      args.push('--resume', resumePath);
    }

    // Handle GitHub username
    if (request.githubUsername) {
      args.push('--github', request.githubUsername);
    }

    // Handle Kaggle URLs
    if (request.kaggleUrls) {
      request.kaggleUrls.forEach(url => {
        args.push('--kaggle', url);
      });
    }

    return new Promise((resolve, reject) => {
      // Try different Python executables in order
      const pythonCommands = ['python3', 'python', '/usr/bin/python3', '/usr/bin/python'];
      let currentCommandIndex = 0;

      const tryNextPython = () => {
        if (currentCommandIndex >= pythonCommands.length) {
          reject(new Error('No working Python executable found'));
          return;
        }

        const pythonCommand = pythonCommands[currentCommandIndex];
        console.log(`Trying Python command: ${pythonCommand}`);

        const pythonProcess = spawn(pythonCommand, args, {
          cwd: skillVerificationPath,
          env: { 
            ...process.env,
            // Add the venv path to make sure it finds the right Python
            PATH: `/mnt/c/Users/koira/Programming/midnight/Midnight/AI-ZK-Agents/.venv/bin:${process.env.PATH}`
          }
        });

        let stdout = '';
        let stderr = '';

        pythonProcess.stdout.on('data', (data) => {
          stdout += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          stderr += data.toString();
        });

        pythonProcess.on('close', async (code) => {
          // Clean up temp files
          if (request.resumeFile) {
            try {
              await fs.unlink(path.join(tempDir, `${request.candidateId}-resume.pdf`));
            } catch (err) {
              console.warn('Failed to clean up resume file:', getErrorMessage(err));
            }
          }

          if (code !== 0) {
            console.error(`${pythonCommand} failed with code ${code}: ${stderr}`);
            if (stderr.includes('ModuleNotFoundError') && currentCommandIndex < pythonCommands.length - 1) {
              currentCommandIndex++;
              tryNextPython();
              return;
            }
            reject(new Error(`SkillVerification failed with code ${code}: ${stderr}`));
            return;
          }

          try {
            const result = JSON.parse(stdout);
            resolve(result);
          } catch (err) {
            reject(new Error(`Failed to parse SkillVerification output: ${getErrorMessage(err)}`));
          }
        });

        pythonProcess.on('error', (err) => {
          console.error(`Failed to spawn ${pythonCommand}:`, err);
          if (currentCommandIndex < pythonCommands.length - 1) {
            currentCommandIndex++;
            tryNextPython();
          } else {
            reject(new Error(`Failed to spawn SkillVerification process: ${getErrorMessage(err)}`));
          }
        });
      };

      tryNextPython();
    });
  }

  // Main function to verify and process skills
  async function addSkillWithVerification(request: SkillVerificationRequest) {
    try {
      // First, verify skills using the Python script
      const verificationResult = await verifySkills(request);
      
      // For now, just return the verification result
      // Later, we can add ZK commitment when the blockchain components are ready
      return {
        verification: verificationResult,
        success: true
      };
    } catch (error) {
      throw new Error(`Skill verification failed: ${getErrorMessage(error)}`);
    }
  }

  return {
    addSkillWithVerification,
    verifySkills,
  };
}

// Export types for use in other files
export type { SkillVerificationRequest, SkillVerificationResult };
