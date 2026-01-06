#!/bin/bash
# Zengeza 4 Rentals - Quick Deployment Script

echo "🚀 Zengeza 4 Rentals - Deployment Script"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the project root."
    exit 1
fi

echo "✅ Project directory confirmed"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run checks
echo "🔍 Running Django checks..."
python manage.py check --deploy

if [ $? -eq 0 ]; then
    echo "✅ All checks passed!"
else
    echo "❌ Checks failed. Please fix issues before deploying."
    exit 1
fi

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "🎉 Your app is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Choose a deployment platform (Heroku, Railway, Render, etc.)"
echo "2. Push your code to GitHub"
echo "3. Connect your repository to the platform"
echo "4. Set environment variables (SECRET_KEY, DATABASE_URL, etc.)"
echo "5. Deploy!"
echo ""
echo "📖 Check DEPLOYMENT.md for detailed instructions"
echo ""
echo "🌐 Your live URL will be something like:"
echo "   https://zengeza4rentals.herokuapp.com"
echo "   https://zengeza4rentals.up.railway.app"
echo "   https://zengeza4rentals.onrender.com"