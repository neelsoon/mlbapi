
//Javascript to hide Diablos Rojos del Mexico and Washington Nationals Prospects

document.addEventListener('DOMContentLoaded', function() {
    // Get all the rows in the table body
    const tableRows = document.querySelectorAll('tbody tr');

    // Loop through each row
    tableRows.forEach(function(row) {
        // Get the team name cell (second cell in the row)
        const teamNameCell = row.cells[1]; // Index 1 corresponds to the Team Name column

        // Check if the team name matches the names you want to hide
        const teamName = teamNameCell.textContent.trim();

        if (teamName === 'Diablos Rojos del Mexico' || teamName === 'Washington Nationals Prospects') {
            // Hide the row if the team name matches
            row.style.display = 'none';
        }
    });
});






document.addEventListener('DOMContentLoaded', function() {
    const teamNameCells = document.querySelectorAll('tbody td:nth-child(2)'); // Select all team name cells
    const modal = document.getElementById('htmlPageModal'); // Reference to the modal element

    teamNameCells.forEach(cell => {
        cell.addEventListener('click', async () => {
            const teamId = cell.dataset.teamId; // Retrieve the team ID from the data attribute
            
            try {
                // Make an API call using fetch to retrieve additional data based on the team ID
                const response = await fetch(`https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1`);
                const data = await response.json();

                // Check if the response data contains valid games
                if (data.dates && data.dates.length > 0) {
                    // Find the game with the specified teamId
                    const game = data.dates[0].games.find(game => {
                        return (
                            (game.teams.away.team.id.toString() === teamId) ||
                            (game.teams.home.team.id.toString() === teamId)
                        );
                    });

                    if (game) {
                        const gamePk = game.gamePk;
                        console.log('GamePk for Team ID', teamId, ':', gamePk);

                        // Update the iframe source URL in the existing modal
                        const iframe = modal.querySelector('iframe');
                        if (iframe) {
                            iframe.src = `https://www.mlb.com/gameday/${gamePk}/preview`;
                        }

                        // Show the modal using Bootstrap modal function
                        var myModal = new bootstrap.Modal(modal);
                        myModal.show();
                    } else {
                        console.log('No game found for Team ID', teamId);
                    }
                } else {
                    console.log('No games available in the response');
                }
            } catch (error) {
                console.error('Error fetching or parsing data:', error);
            }
        });
    });
});

