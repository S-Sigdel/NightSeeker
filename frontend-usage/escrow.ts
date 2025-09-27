import { initEscrowMiddleware } from './middleware';
import { getWallet } from '@midnight-ntwrk/wallet'; // Example wallet connector

async function setup() {
  const wallet = await getWallet();
  const config = { /* proof server, indexer, etc. */ };
  const escrow = await initEscrowMiddleware(wallet, config);

  // Example: Fund escrow
  document.getElementById('fundBtn').onclick = async () => {
    const commitment = /* generate commitment off-chain */;
    await escrow.fundEscrow(commitment);
    alert('Escrow funded!');
  };

  // Example: Release payment
  document.getElementById('releaseBtn').onclick = async () => {
    await escrow.releasePayment();
    alert('Payment released!');
  };
}
