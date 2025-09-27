import { initSkillsMiddleware } from './skillsMiddleware';
import { getWallet } from '@midnight-ntwrk/wallet';

async function setup() {
  const wallet = await getWallet();
  const config = { /* proof server, indexer, etc. */ };
  const skills = await initSkillsMiddleware(wallet, config);

  // Add/update skill commitment
  document.getElementById('addSkillBtn').onclick = async () => {
    const commitment = /* generate commitment off-chain */;
    await skills.addSkill(commitment);
    alert('Skill commitment added!');
  };

  // Prove skill knowledge
  document.getElementById('proveSkillBtn').onclick = async () => {
    await skills.proveSkill();
    alert('Skill proof submitted!');
  };
}
