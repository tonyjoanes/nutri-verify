using Microsoft.AspNetCore.Mvc;

namespace NutriVerify.Api.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class ResearchController : ControllerBase
    {
        private readonly ILogger<ResearchController> _logger;

        public ResearchController(ILogger<ResearchController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult GetResearch([FromQuery] string? dietType = null)
        {
            // Temporary mock data
            var mockPapers = new[]
            {
                new
                {
                    Id = 1,
                    Title = "Effects of Ketogenic Diet on Weight Loss",
                    Authors = new[] { "Smith, J.", "Johnson, M." },
                    DietType = "keto",
                    PublicationDate = DateTime.Parse("2024-01-15"),
                    Source = "PubMed"
                },
                new
                {
                    Id = 2,
                    Title = "Comparative Analysis of Low-Carb Diets",
                    Authors = new[] { "Brown, R.", "Davis, K." },
                    DietType = "low-carb",
                    PublicationDate = DateTime.Parse("2024-02-01"),
                    Source = "NIH"
                }
            };

            if (!string.IsNullOrEmpty(dietType))
            {
                var filteredPapers = mockPapers.Where(p =>
                    p.DietType.Equals(dietType, StringComparison.OrdinalIgnoreCase));
                return Ok(filteredPapers);
            }

            return Ok(mockPapers);
        }

        [HttpGet("{id}")]
        public IActionResult GetResearchById(int id)
        {
            // Mock detailed paper data
            var paper = new
            {
                Id = id,
                Title = "Effects of Ketogenic Diet on Weight Loss",
                Authors = new[] { "Smith, J.", "Johnson, M." },
                DietType = "keto",
                PublicationDate = DateTime.Parse("2024-01-15"),
                Source = "PubMed",
                Abstract = "A comprehensive study on the effects of ketogenic diet...",
                Methodology = "Randomized controlled trial with 200 participants...",
                Findings = new[]
                {
                "Significant weight loss observed in 75% of participants",
                "Improved insulin sensitivity in diabetic participants",
                "Reduced inflammation markers in blood tests"
            }
            };

            return Ok(paper);
        }

        [HttpPost("verify-claim")]
        public IActionResult VerifyClaim([FromBody] ClaimVerificationRequest request)
        {
            _logger.LogInformation("Claim verification requested for: {Claim}", request.Claim);

            // Mock verification response
            var response = new
            {
                Claim = request.Claim,
                VerificationStatus = "Partially Verified",
                ConfidenceScore = 0.75,
                SupportingEvidence = new[]
                {
                    new
                    {
                        PaperId = 1,
                        Title = "Effects of Ketogenic Diet on Weight Loss",
                        Relevance = "High",
                        FindingsSummary = "Supports the claim with some caveats..."
                    }
                },
                    Context = "This claim requires additional context...",
                    Limitations = new[]
                    {
                    "Limited study duration",
                    "Small sample size"
                    }
            };

            return Ok(response);
        }
    }
}

public class ClaimVerificationRequest
{
    public string Claim { get; set; } = string.Empty;
    public string? Source { get; set; }
    public string? Context { get; set; }
}