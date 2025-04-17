import os
import subprocess

# Paths for the Scrapy and Selenium script directories
scrapy_dir = r"G:\Vyoma\vyoma_scraper\vyoma_scraper\spiders\spider files"
selenium_dir = r"G:\Vyoma\vyoma_scraper\selenium files"

def run_scrapy_scripts():
    """Run all Scrapy spiders inside the scrapy directory."""
    print("\n🚀 Running Scrapy spiders...\n")
    for file in os.listdir(scrapy_dir):
        if file.endswith(".py") and file != "run_all_scrapers.py":  # Ignore the master script itself
            script_path = os.path.join(scrapy_dir, file)
            print(f"▶ Running Scrapy spider: {file}")
            subprocess.run(["python", script_path], cwd=scrapy_dir)

def run_selenium_scripts():
    """Run all Selenium scripts inside the selenium directory."""
    print("\n🚀 Running Selenium scripts...\n")
    for file in os.listdir(selenium_dir):
        if file.endswith(".py"):
            script_path = os.path.join(selenium_dir, file)
            print(f"▶ Running Selenium script: {file}")
            subprocess.run(["python", script_path], cwd=selenium_dir)

if __name__ == "__main__":
    print("=====================================")
    print("  🔄 Starting Master Script Execution")
    print("=====================================\n")

    run_scrapy_scripts()
    run_selenium_scripts()

    print("\n✅ All scripts executed successfully!")
