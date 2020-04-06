using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;


namespace URL_Map
{   
    [TestFixture] 
    public class Tests
    {
        IWebDriver driver;
        [OneTimeSetUp]
        public void Setup()
        {
            driver = new ChromeDriver();
        }

        [Test]
        public void Test1()
        {
            Assert.Pass();
        }
        [OneTimeTearDown]
        public void Close()
        {
           // driver.Close();

        }
    }
}