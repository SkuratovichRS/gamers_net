import { logout, checkAuth, getAllUsers } from '../api/auth.js';
import { getUserGames, addUserGame } from '../api/games.js';
import { showNotification } from '../components/notification.js';

async function checkAuthentication() {
    try {
        const response = await checkAuth();
        if (!response.ok) {
            window.location.replace('http://localhost:8080/');
            return false;
        }
        document.body.style.display = 'block';
        return true;
    } catch (error) {
        console.error('Auth check failed:', error);
        window.location.replace('http://localhost:8080/');
        return false;
    }
}

async function fetchUsers() {
    try {
        const response = await getAllUsers();
        
        if (response.ok) {
            const users = await response.json();
            displayUsers(users);
        } else {
            showNotification('Failed to fetch users');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error fetching users');
    }
}

async function fetchUserGames() {
    try {
        const response = await getUserGames();
        
        if (response.ok) {
            const games = await response.json();
            displayGames(games);
        } else {
            showNotification('Failed to fetch games');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error fetching games');
    }
}

function displayUsers(users) {
    const usersList = document.getElementById('users-list');
    usersList.innerHTML = '';
    
    users.forEach(user => {
        const li = document.createElement('li');
        li.className = 'data-item';
        li.textContent = `Nickname: ${user.nickname} | Email: ${user.email}`;
        usersList.appendChild(li);
    });
    
    document.getElementById('users-container').style.display = 'block';
    document.getElementById('games-container').style.display = 'none';
    document.getElementById('game-form').style.display = 'none';
}

function displayGames(games) {
    const gamesList = document.getElementById('games-list');
    gamesList.innerHTML = '';
    
    games.forEach(game => {
        const li = document.createElement('li');
        li.className = 'data-item';
        li.textContent = `Game: ${game.game_name}`;
        gamesList.appendChild(li);
    });
    
    document.getElementById('games-container').style.display = 'block';
    document.getElementById('users-container').style.display = 'none';
    document.getElementById('game-form').style.display = 'none';
}

async function handleAddGame() {
    const gameNameInput = document.getElementById('game-name');
    const gameName = gameNameInput.value.trim();
    const errorElement = document.getElementById('game-error');
    
    errorElement.style.display = 'none';
    
    if (!gameName) {
        errorElement.textContent = 'Please enter a game name';
        errorElement.style.display = 'block';
        return;
    }

    try {
        const response = await addUserGame(gameName);
        
        if (response.ok) {
            showNotification('Game added successfully!');
            gameNameInput.value = '';
            await fetchUserGames();
        } else {
            const data = await response.json();
            handleAddGameError(response.status, data, errorElement);
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error adding game');
    }
}

function handleAddGameError(status, data, errorElement) {
    if (status === 404) {
        errorElement.textContent = 'Game not found in our database';
    } else if (status === 409) {
        errorElement.textContent = 'You already have this game';
    } else {
        errorElement.textContent = data.detail || 'Failed to add game';
    }
    errorElement.style.display = 'block';
}

function initializeEventListeners() {
    document.getElementById('show-users-btn').addEventListener('click', fetchUsers);
    document.getElementById('show-games-btn').addEventListener('click', fetchUserGames);
    document.getElementById('add-game-btn').addEventListener('click', toggleGameForm);
    document.getElementById('submit-game-btn').addEventListener('click', handleAddGame);
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    
    document.getElementById('game-name').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            handleAddGame();
        }
    });
}

function toggleGameForm() {
    const gameForm = document.getElementById('game-form');
    const usersContainer = document.getElementById('users-container');
    const gamesContainer = document.getElementById('games-container');
    
    gameForm.style.display = gameForm.style.display === 'none' ? 'block' : 'none';
    usersContainer.style.display = 'none';
    gamesContainer.style.display = 'none';
}

async function handleLogout() {
    try {
        const response = await logout();
        if (response.ok) {
            window.location.href = 'http://localhost:8080/';
        } else {
            showNotification('Failed to log out');
        }
    } catch (error) {
        console.error('Error:', error);
        showNotification('Error during log out');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', async () => {
    if (await checkAuthentication()) {
        initializeEventListeners();
    }
});
