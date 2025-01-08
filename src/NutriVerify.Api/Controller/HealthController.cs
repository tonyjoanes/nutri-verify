using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;

namespace NutriVerify.Api.Controller
{
    [ApiController]
    [Route("api/[controller]")]
    public class HealthController : ControllerBase
    {
        private readonly ILogger<HealthController> _logger;

        public HealthController(ILogger<HealthController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Get()
        {
            return Ok(new
            {
                Status = "Healthy",
                Timestamp = DateTime.UtcNow,
                Version = "1.0.0"
            });
        }

        [HttpGet("details")]
        public IActionResult GetDetails()
        {
            var healthDetails = new
            {
                Status = "Healthy",
                Timestamp = DateTime.UtcNow,
                Version = "1.0.0",
                Environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT"),
                Runtime = Environment.Version.ToString(),
                ProcessUptime = (DateTime.Now - Process.GetCurrentProcess().StartTime).ToString()
            };

            _logger.LogInformation("Health check details requested at {Timestamp}", DateTime.UtcNow);
            return Ok(healthDetails);
        }
    }
}