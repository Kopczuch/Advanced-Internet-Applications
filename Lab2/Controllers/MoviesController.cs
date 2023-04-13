using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Numerics;

namespace Lab2.Controllers;
[ApiController]
[Route("[controller]")]
public class MoviesController : ControllerBase
{
    MoviesContext dbContext = new MoviesContext();

    // Method for uploading movies via csv file
    [HttpPost("UploadMovieCsv")]
    public string Post(IFormFile inputFile)
    {
        var strm = inputFile.OpenReadStream();
        byte[] buffer = new byte[inputFile.Length];
        strm.Read(buffer, 0, (int)inputFile.Length);
        string fileContent = System.Text.Encoding.Default.GetString(buffer);
        strm.Close();
        List<Movie> tempMovies = new List<Movie>();
        bool skip_header = true;
        foreach (string line in fileContent.Split('\n'))
        {
            if (skip_header)
            {
                skip_header = false;
                continue;
            }
            var tokens = Regex.Split(line, ",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");
            //var tokens = line.Split(",");
            if (tokens.Length != 3) continue;
            string MovieID = tokens[0];
            string MovieName = tokens[1].Trim('"');
            string[] Genres = tokens[2].Split("|").Select(genre => genre.Trim('\r', '\n')).ToArray();;

            List<Genre> movieGenres = new List<Genre>();
            foreach (string genre in Genres)
            {
                Genre g = new Genre();
                g.Name = genre;
                if (!dbContext.Genres.Any(e => e.Name == g.Name))
                {
                    dbContext.Genres.Add(g);
                    dbContext.SaveChanges();
                }
                IQueryable<Genre> results = dbContext.Genres.Where(e => e.Name == g.Name);
                if (results.Count() > 0)
                    movieGenres.Add(results.First());
            }

            if (!tempMovies.Any(e => e.MovieID == int.Parse(MovieID)) && !dbContext.Movies.Any(e => e.MovieID == int.Parse(MovieID)))
            {
                Movie m = new Movie();
                m.MovieID = int.Parse(MovieID);
                m.Title = MovieName;
                m.Genres = movieGenres;
                tempMovies.Add(m);
            }
        }
        dbContext.AddRange(tempMovies);
        dbContext.SaveChanges();

        return "OK";
    }

    // Method for uploading ratings via csv file
    [HttpPost("UploadRatingsCsv")]
    public string PostRatings(IFormFile inputFile)
    {
        var strm = inputFile.OpenReadStream();
        byte[] buffer = new byte[inputFile.Length];
        strm.Read(buffer, 0, (int)inputFile.Length);
        string fileContent = System.Text.Encoding.Default.GetString(buffer);
        strm.Close();

        bool skip_header = true;
        List<User> tempUsers = new List<User>();
        List<Rating> tempRatings = new List<Rating>();

        foreach (string line in fileContent.Split('\n'))
        {
            if (skip_header)
            {
                skip_header = false;
                continue;
            }

            var tokens = line.Split(",");
            if (tokens.Length != 4) continue;
            string idstr = tokens[0];
            int id = int.Parse(idstr);

            if (!tempUsers.Any(e => e.UserID == id) && !dbContext.Users.Any(e => e.UserID == id))
            {
                User u = new User();
                u.UserID = id;
                u.Name = "User" + idstr;
                tempUsers.Add(u);
            }
        }

        dbContext.Users.AddRange(tempUsers);
        dbContext.SaveChanges();

        skip_header = true;
        foreach (string line in fileContent.Split('\n'))
        {
            if (skip_header)
            {
                skip_header = false;
                continue;
            }

            var tokens = line.Split(",");
            if (tokens.Length != 4) continue;
            
            Rating r = new Rating();
            r.RatingUser = dbContext.Users.Where(e => e.UserID == int.Parse(tokens[0])).First();
            r.RatedMovie = dbContext.Movies.FirstOrDefault(e => e.MovieID == int.Parse(tokens[1]));
            r.RatingValue = tokens[2];
            if (r.RatedMovie != null) tempRatings.Add(r);
        }

        dbContext.AddRange(tempRatings);
        dbContext.SaveChanges();

        return "OK";
    }

    // Method returning all genres
    [HttpGet("GetAllGenres")]
    public IEnumerable<Genre> GetAllGenres()
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Genres.AsEnumerable();
    }
    
    // Method returning all ratings
    [HttpGet("GetAllRatings")]
    public IEnumerable<Rating> GetAllRatings()
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Ratings.AsEnumerable();
    }

    // Method returning movie with given name
    [HttpGet("GetMoviesByName/{search_phrase}")]
    public IEnumerable<Movie> GetMoviesByName(string search_phrase)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies.Where(e => e.Title.Contains(search_phrase));
    }

    // Method returning movies with a given genre
    [HttpGet("GetMoviesByGenre")]
    public IEnumerable<Movie> GetMoviesByGenre(string search_phrase)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies.Where(
            m => m.Genres.Any(p => p.Name.Contains(search_phrase))
        );
    }

    // Method returning genres of a movie with given id
    [HttpGet("GetMovieGenres/{movie_id}")]
    public IEnumerable<Genre> GetMovieGenres(int movie_id)
    {
        MoviesContext dbContext = new MoviesContext();
        return dbContext.Movies
            .Include(e => e.Genres)
            .FirstOrDefault(e => e.MovieID == movie_id).Genres;
    }

    // Method creating genre vector of a movie with given id
    [HttpGet("GetGenresVector/{movie_id}")]
    public List<int> GetGenresVector(int movie_id)
    {
        MoviesContext dbContext = new MoviesContext();
        List<Genre> AllGenres = dbContext.Genres
            .Where(e => e.Name != "(no genres listed)")
            .OrderBy(e => e.Name)
            .ToList();
        
        List<int> GenreVector = Enumerable.Repeat(0, AllGenres.Count()).ToList();

        List<Genre> MovieGenres = GetMovieGenres(movie_id).ToList();
        int count = 0;
        foreach (var genre in AllGenres)
        {
            bool containsGenre = MovieGenres.Any(e => e.Name == genre.Name);
            if (containsGenre)
            {
                GenreVector[count] = 1;
            }
            count++;
        }

        return GenreVector;
    }

    // Method calculating cosine similarity of two vectors
    public static double CosineSimilarity(List<int> v1, List<int> v2)
    {
        if (v1.Count() != v2.Count())
        {
            throw new ArgumentException("Vectors must be of the same lenght.");
        }
        
        double dotProduct = 0.0;
        double mag1 = 0.0;
        double mag2 = 0.0;

        for (int i = 0; i < v1.Count(); i++)
        {
            dotProduct += (double)v1[i] * (double)v2[i];
            mag1 += Math.Pow((double)v1[i], 2);
            mag2 += Math.Pow((double)v2[i], 2);
        }

        mag1 = Math.Sqrt(mag1);
        mag2 = Math.Sqrt(mag2);

        //return dotProduct / (mag1 * mag2);
        return Math.Round(dotProduct / (mag1 * mag2), 4);
    }

    // Method comparing two movies with given id using cosine similarity
    [HttpGet("CompareMovies/{movie1_id, movie2_id}")]
    public double CompareMovies(int movie1_id, int movie2_id)
    {
        List<int> v1 = GetGenresVector(movie1_id);
        List<int> v2 = GetGenresVector(movie2_id);
        return CosineSimilarity(v1, v2);
    }

    // Method returning list of movies with at least one shared genre
    [HttpGet("SharedGenreMovies/{movie_id}")]
    public List<Movie> SharedGenreMovies(int movie_id)
    {
        MoviesContext dbContext = new MoviesContext();
        var movie = dbContext.Movies
            .Include(e => e.Genres)
            .FirstOrDefault(e => e.MovieID == movie_id);

        List<Movie> SharedGenreMovies = dbContext.Movies
            .Include(e => e.Genres)
            .Where(e => e.Genres.Any(f => movie.Genres.Contains(f)))
            .ToList();

        return SharedGenreMovies;
    }

    // Method returning list of movies with similarity over a given threshold
    [HttpGet("SimilarMovies/{movie_id, threshold}")]
    public List<Movie> SimilarMovies(int movie_id, double threshold)
    {
        MoviesContext dbContext = new MoviesContext();
        List<Movie> AllMovies = dbContext.Movies.ToList();
        List<Movie> Result = new List<Movie>();

        foreach (var movie in AllMovies)
        {
            if (CompareMovies(movie_id, movie.MovieID) > threshold)
            {
                if (movie_id == movie.MovieID)
                    continue;
                Result.Add(movie);
            }
        }

        return Result;
    }

    // Method returning movies rated by user with given id
    [HttpGet("RatedByUser/{user_id}")]
    public List<Movie> RatedByUser(int user_id)
    {
        MoviesContext dbContext = new MoviesContext();
        List<Rating> Ratings = dbContext.Ratings
            .Where(e => e.RatingUser.UserID == user_id)
            .ToList();
        TODO:
        // List<Movie> RatedMovies = dbContext.Movies
        //     .Where(e => Ratings.Contains(e.MovieID))
        //     .ToList();
        return new List<Movie>();
    }

    // Method returning movies rated by user with given id sorted by rating
    [HttpGet("RatedByUserSorted/{user_id}")]
    public List<Movie> RatedByUserSorted(int user_id)
    {
        
        return new List<Movie>();
    }

}