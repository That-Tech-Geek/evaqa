// nodes/voting_logic.function.js
// EVAQA Council Voting Node
// Implements Sovereign Voting: any BLOCK stops the deal, 4+ APPROVE + 0 BLOCK → AUTO-WIRE

module.exports = {
    description: 'Aggregates votes from AI Agents and determines verdict',
    defaults: {
        name: 'CouncilVoting',
        color: '#1F6FEB',
    },
    inputs: ['main'],
    outputs: ['main'],
    execute: async function() {
        const items = this.getInputData();
        const run_id = this.getNodeParameter('run_id', 0);

        // Extract votes
        let votes = items.map(i => i.json.vote); // Expected format: {agent: 'Hawk', vote: 'APPROVE/BLOCK/WATCH', reason: ''}
        let approve = 0;
        let block = 0;
        let watch = 0;

        votes.forEach(v => {
            switch(v.vote) {
                case 'APPROVE': approve++; break;
                case 'BLOCK': block++; break;
                case 'WATCH': watch++; break;
            }
        });

        // Determine verdict
        let verdict = 'HUMAN_INTERVENTION';
        if(block > 0) verdict = 'BLOCK';
        else if(approve >= 4 && block === 0) verdict = 'AUTO_WIRE';
        else verdict = 'HUMAN_INTERVENTION';

        return this.prepareOutputData([{
            json: {
                run_id,
                votes,
                approve,
                block,
                watch,
                verdict,
                timestamp: new Date().toISOString()
            }
        }]);
    }
};
