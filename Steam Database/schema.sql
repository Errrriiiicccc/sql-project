USE SteamDatabaseDEV;

CREATE TABLE Games (
    GameId INT PRIMARY KEY,          -- Steam App ID
    Name NVARCHAR(200) NOT NULL,
    ReleaseDate DATETIME NULL,
    IsFree BIT NULL,
    Price DECIMAL(10,2) NULL,
    LastUpdated DATETIME DEFAULT GETDATE()
);

CREATE TABLE GameSnapshots (
    SnapshotId INT IDENTITY(1,1) PRIMARY KEY,
    GameId INT NOT NULL,

    PlayersCurrent INT NULL,
    PlayersPeak INT NULL,

    MetacriticScore INT NULL,

    SnapshotTime DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (GameId) REFERENCES Games(GameId)
);

CREATE TABLE Genres (
    GenreId INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE GameGenres (
    GameId INT,
    GenreId INT,

    PRIMARY KEY (GameId, GenreId),

    FOREIGN KEY (GameId) REFERENCES Games(GameId),
    FOREIGN KEY (GenreId) REFERENCES Genres(GenreId)
);