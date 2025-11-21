# NightSeeker - Anonymous Talent Matching Platform

A revolutionary blockchain-powered employment platform built on the Midnight Network that enables completely anonymous talent matching between employers and skilled professionals while ensuring skill authenticity and secure payments.

## 🌙 What is NightSeeker?

NightSeeker leverages the Midnight Network's zero-knowledge cryptography to create the first truly anonymous employment marketplace where:

- **Employees remain completely anonymous** - not even platform administrators know user identities
- **Skills are cryptographically verified** - AI-powered skill verification with ZK proofs ensures authenticity
- **Payments are private and secure** - anonymous transactions powered by Midnight's privacy technology
- **Employers can hire with confidence** - verified skills without compromising candidate privacy
- **Smart matching algorithm** - connects the right talent with the right opportunities anonymously

## 🔒 Core Privacy Features

### Zero-Knowledge Identity Protection
- **Complete Anonymity**: User identities are never stored or accessible to anyone, including administrators
- **ZK-Proof Verification**: Skills are verified using zero-knowledge proofs without revealing personal information
- **Anonymous Communication**: Encrypted messaging between employers and candidates without identity exposure

### Private Skill Verification
- **AI-Powered Analysis**: Upload resumes and GitHub profiles for automated skill extraction and verification
- **Cryptographic Commitments**: Skills are committed to the blockchain without revealing sensitive data
- **Verifiable Claims**: Employers can verify skill authenticity without accessing personal information

### Secure Anonymous Payments
- **Private Transactions**: All payments processed through Midnight Network's privacy-preserving protocol
- **Escrow Protection**: Smart contract escrow ensures payment security for both parties
- **Anonymous Earnings**: Income tracking without linking to real-world identities

## 🚀 Key Features

### For Job Seekers
- **Anonymous Profile Creation**: Build professional profiles without revealing identity
- **AI Skill Verification**: Upload resumes/portfolios for automated skill analysis and verification
- **Privacy-First Job Search**: Browse and apply for jobs while maintaining complete anonymity
- **Secure Communication**: Encrypted messaging with potential employers
- **Anonymous Payment Reception**: Receive payments directly to anonymous wallets

### For Employers
- **Anonymous Job Posting**: Post opportunities without revealing company identity
- **Verified Talent Pool**: Access candidates with cryptographically verified skills
- **Smart Matching**: AI algorithm suggests best-fit candidates based on verified skills
- **Secure Hiring Process**: Complete hiring workflow with zero-knowledge verification
- **Anonymous Payment Processing**: Pay contractors securely through privacy-preserving protocol

### Platform Features
- **Demo Mode**: Try the platform without connecting a wallet
- **Real-time Skill Matching**: Advanced algorithms match candidates to relevant opportunities
- **Reputation System**: Build anonymous reputation through completed work and endorsements
- **Multi-platform Verification**: GitHub, resume, and portfolio analysis for comprehensive skill verification

## 🛠 Technology Stack

### Frontend
- **React + TypeScript**: Modern, type-safe user interface
- **Wagmi + Web3Modal**: Seamless Web3 wallet integration
- **MidnightJS**: Native Midnight Network wallet integration and transaction handling
- **Tailwind CSS**: Responsive, modern design system
- **React Router**: Client-side routing for smooth navigation

### Blockchain & Privacy
- **Midnight Network**: Privacy-preserving blockchain for anonymous transactions
- **Compact Language**: Midnight's smart contract language for ZK applications
- **Zero-Knowledge Proofs**: Cryptographic verification without data exposure
- **Smart Contracts**: Automated escrow, jobs, and reputation management
- **Anonymous Commitments**: Skill and identity commitments using ZK technology
- **Commitment/Nullifier Pattern**: Privacy-preserving state updates and authentication

### Smart Contract Architecture
- **Jobs Contract**: Anonymous job posting and verification using ZK commitments
- **Escrow Contract**: Privacy-preserving payment escrow with ZK proof releases
- **Reputation Contract**: Anonymous endorsement system with cryptographic commitments
- **Skills Contract**: Skill verification and commitment storage with ZK proofs

### AI & Verification
- **OpenAI Integration**: Advanced language models for skill analysis
- **GitHub API**: Repository analysis for skill verification
- **PDF Processing**: Resume parsing and skill extraction
- **Machine Learning**: Intelligent job-candidate matching algorithms

### Backend Infrastructure
- **Node.js + Express**: RESTful API server
- **Python Integration**: AI processing and skill verification scripts
- **Midnight SDK**: Backend integration with Midnight Network contracts
- **File Processing**: Secure resume and document handling
- **Database Privacy**: Encrypted storage with zero-knowledge architecture

## 🏗 Project Structure

```
Midnight/
├── midnight-frontend/          # React frontend application
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   │   └── Layout/        # Header, navigation, and layout components
│   │   ├── pages/            # Main application pages
│   │   │   ├── Home.tsx      # Landing page with features
│   │   │   ├── Profile.tsx   # User profile and skill verification
│   │   │   ├── Jobs.tsx      # Job browsing and search
│   │   │   ├── CurrentJobs.tsx # Active job management
│   │   │   └── Reputation.tsx # Reputation and endorsements
│   │   ├── hooks/            # Custom React hooks
│   │   ├── services/         # API integration and services
│   │   ├── config/           # Web3 and MidnightJS configuration
│   │   ├── data/             # Mock data for demo mode
│   │   └── types/            # TypeScript definitions
├── middleware-api/            # Express backend server
│   ├── src/
│   │   ├── routes/           # API route handlers
│   │   │   ├── skills.ts     # AI skill verification middleware
│   │   │   ├── jobs.ts       # Jobs contract integration
│   │   │   ├── escrow.ts     # Escrow contract middleware
│   │   │   └── reputation.ts # Reputation system middleware
│   │   └── server.ts         # Main server configuration
├── contracts/                 # Compact smart contracts
│   ├── Jobs.compact          # Anonymous job posting and management
│   ├── Escrow.compact        # Privacy-preserving payment escrow
│   └── Reputation.compact    # Anonymous reputation and endorsements
├── AI-ZK-Agents/             # AI skill verification system
│   ├── SkillVerification/    # Core verification algorithms
│   │   └── core.py          # Main skill analysis and LLM integration
│   └── scripts/              # Processing and test scripts
│       └── test_skill_verification.py
└── frontend-usage/           # Midnight Network integration examples
    ├── skills.ts             # Skills contract usage examples
    ├── jobs.ts               # Jobs contract integration examples
    ├── escrow.ts             # Escrow workflow examples
    └── reputation.ts         # Reputation system examples
```

## 🚦 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- Git
- Midnight Network compatible wallet

### Environment Setup
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Midnight
   ```

2. **Configure environment variables**
   ```bash
   # Copy and configure environment file
   cp .env.example .env
   
   # Add your API keys:
   OPENAI_API_KEY=your_openai_api_key
   GITHUB_TOKEN=your_github_token
   VITE_WALLET_CONNECT_PROJECT_ID=your_walletconnect_project_id
   ```

3. **Install Python dependencies**
   ```bash
   cd AI-ZK-Agents
   pip install python-dotenv openai PyGithub pandas numpy scikit-learn PyPDF2 pdfplumber
   ```

4. **Setup backend server**
   ```bash
   cd middleware-api
   npm install
   npm run dev  # Runs on http://localhost:3001
   ```

5. **Launch frontend application**
   ```bash
   cd midnight-frontend
   npm install
   npm run dev  # Runs on http://localhost:5173
   ```

### Testing the Platform
1. **Try Demo Mode**: Experience the platform without wallet connection
2. **Upload Skills**: Test AI verification with resume/GitHub profile (requires middleware API running)
3. **Browse Jobs**: Explore anonymous job opportunities
4. **Connect Wallet**: For full anonymous functionality (requires Midnight Network wallet)

## 🎯 How It Works

### Smart Contract Architecture

#### Jobs Contract (`Jobs.compact`)
- **Anonymous Job Creation**: Employers submit cryptographic commitments to job data
- **ZK Job Verification**: Prove job properties without revealing sensitive information
- **Privacy-Preserving Matching**: Match candidates based on encrypted requirements

#### Escrow Contract (`Escrow.compact`)
- **Commitment-Based Escrow**: Funds locked using cryptographic commitments
- **ZK Payment Release**: Release payments with zero-knowledge proofs
- **Nullifier Prevention**: Prevent double-spending using unique nullifiers

#### Reputation Contract (`Reputation.compact`)
- **Anonymous Endorsements**: Submit endorsements without revealing identities
- **Cryptographic Commitments**: Store reputation data as commitments
- **ZK Reputation Proofs**: Prove reputation levels without exposing details

### Skill Verification Process
1. **Upload Evidence**: Submit resume, GitHub profile, or portfolio
2. **AI Analysis**: Advanced algorithms extract and analyze skills using OpenAI
3. **ZK Commitment**: Skills committed to blockchain with zero-knowledge proofs
4. **Verification**: Cryptographic verification without revealing personal data

### Anonymous Job Matching
1. **Profile Creation**: Build anonymous professional profile with verified skills
2. **Smart Matching**: AI algorithm suggests relevant opportunities
3. **Anonymous Application**: Apply for jobs while maintaining complete privacy
4. **Secure Communication**: Encrypted messaging throughout hiring process

### Privacy-Preserving Payments
1. **Smart Escrow**: Funds held in Compact smart contracts
2. **Milestone Payments**: Payments released based on work completion using ZK proofs
3. **Anonymous Transactions**: All payments processed through Midnight Network
4. **Reputation Building**: Anonymous feedback and reputation accumulation

## 🔐 Privacy Guarantees

- **Zero Data Collection**: No personal information stored or accessible
- **Cryptographic Verification**: All claims verified using zero-knowledge proofs
- **Anonymous Transactions**: Complete financial privacy through Midnight Network
- **Secure Communication**: End-to-end encrypted messaging
- **Verifiable Skills**: Authentic skill verification without identity exposure
- **Commitment/Nullifier Pattern**: Industry-standard privacy-preserving architecture

## 🌟 Why NightSeeker?

- **True Anonymity**: First employment platform with complete identity protection powered by Midnight Network
- **Verified Talent**: Cryptographically proven skills eliminate fake profiles
- **Global Access**: Work opportunities without geographic or identity barriers
- **Secure Payments**: Anonymous, fast, and secure compensation using Compact contracts
- **Fair Matching**: Algorithm-based matching ensures merit-based hiring
- **Privacy by Design**: Built from ground up with zero-knowledge architecture

## 🔧 Technical Implementation

### Compact Smart Contracts
Our platform uses Midnight Network's Compact language to implement privacy-preserving smart contracts:

- **Commitment Schemes**: Store encrypted data commitments on-chain
- **Zero-Knowledge Circuits**: Verify computations without revealing inputs
- **Nullifier Systems**: Prevent double-spending and replay attacks
- **Witness-Based Proofs**: Private inputs validated through ZK proofs

### MidnightJS Integration
- **Wallet Connection**: Native Midnight Network wallet integration
- **Transaction Handling**: Seamless ZK transaction processing
- **Contract Interaction**: Direct communication with Compact contracts
- **Proof Generation**: Client-side zero-knowledge proof creation

### AI-Powered Verification
- **Resume Analysis**: PDF parsing and skill extraction
- **GitHub Integration**: Repository analysis for skill verification
- **LLM Processing**: Advanced language models for skill assessment
- **Confidence Scoring**: Machine learning-based skill confidence ratings

## 🛣 Roadmap

- ✅ **Phase 1**: Core platform with AI skill verification
- 🔄 **Phase 2**: Full Midnight Network integration for complete anonymity
- 📋 **Phase 3**: Advanced matching algorithms and reputation system
- 📱 **Phase 4**: Mobile application and expanded verification methods
- 🏛️ **Phase 5**: Decentralized governance and community features

## 🤝 Contributing

We welcome contributions to make anonymous employment accessible globally. Please read our contributing guidelines and feel free to submit issues and pull requests.

### Development Setup
1. Follow the getting started guide above
2. Review the Compact contract documentation
3. Test with demo mode before wallet integration
4. Ensure all ZK proofs are properly validated

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Midnight Network](https://midnight.network/)
- [Compact Language Documentation](https://docs.midnight.network/)
- [MidnightJS SDK](https://docs.midnight.network/develop/sdks/midnightjs)
- [Zero-Knowledge Proofs Guide](https://docs.midnight.network/develop/how-midnight-works/keeping-data-private)

---

**Built with privacy in mind. Powered by Midnight Network. 🌙**

*Experience true anonymity in professional networking with cryptographically verified skills and zero-knowledge payments.*
