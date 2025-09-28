import express from 'express';
import cors from 'cors';
import multer from 'multer';
import { initSkillsMiddleware } from './routes/skills';

const app = express();
const port = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Configure multer for file uploads
const upload = multer({ 
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 } // 10MB limit
});

// Initialize skills middleware
let skillsMiddleware: any;
initSkillsMiddleware().then(middleware => {
  skillsMiddleware = middleware;
}).catch(console.error);

// Skills verification endpoint
app.post('/api/skills/verify', upload.single('resumeFile'), async (req, res) => {
  try {
    if (!skillsMiddleware) {
      return res.status(500).json({ error: 'Skills middleware not initialized' });
    }

    const { candidateId, githubUsername } = req.body;
    const resumeFile = req.file;

    console.log('📥 Received skill verification request:', {
      candidateId,
      githubUsername,
      hasResumeFile: !!resumeFile
    });

    const request = {
      candidateId,
      resumeFile: resumeFile?.buffer,
      githubUsername: githubUsername || undefined,
    };

    const result = await skillsMiddleware.addSkillWithVerification(request);
    
    console.log('✅ Skill verification successful:', result);
    res.json(result);

  } catch (error) {
    console.error('❌ Skill verification error:', error);
    res.status(500).json({ 
      error: 'Skill verification failed',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', timestamp: new Date().toISOString() });
});

app.listen(port, () => {
  console.log(`🚀 Middleware API server running on http://localhost:${port}`);
});