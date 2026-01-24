# Test the /api/analyze endpoint with curl
# Make sure the backend is running first: uvicorn app.main:app --reload

Write-Host "Testing /api/analyze endpoint..." -ForegroundColor Cyan
Write-Host ""

$body = @{
    listing_data = @{
        title = "Spacious 3BHK Apartment in Prime Location"
        description = "Beautiful 3BHK apartment with modern amenities, parking, and great view"
        price = 5000000
        area_sqft = 1500
        city = "Mumbai"
        locality = "Andheri West"
        latitude = 19.1334
        longitude = 72.8291
    }
} | ConvertTo-Json -Depth 3

Write-Host "Request Body:" -ForegroundColor Yellow
Write-Host $body
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/analyze" -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Yellow
    $response | ConvertTo-Json -Depth 3
    Write-Host ""
    
    # Validate response structure
    if ($response.fraud_probability -ne $null -and 
        $response.fraud_types -ne $null -and 
        $response.explanations -ne $null) {
        Write-Host "✅ Response structure is valid!" -ForegroundColor Green
    } else {
        Write-Host "❌ Response structure is invalid!" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Make sure the backend server is running:" -ForegroundColor Yellow
    Write-Host "  cd backend" -ForegroundColor Cyan
    Write-Host "  .\\venv\\Scripts\\activate" -ForegroundColor Cyan
    Write-Host "  uvicorn app.main:app --reload" -ForegroundColor Cyan
}
