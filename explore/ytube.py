# pip install yt-dlp
import subprocess

def download_youtube_playlist(playlist_url, download=True):
    if not playlist_url.startswith("http"):
        print("Invalid playlist URL.")
        return

    # Base yt-dlp command
    base_cmd = ["yt-dlp", playlist_url]

    if not download:
        # Just print video titles and URLs
        base_cmd += ["--flat-playlist", "-J"]

        try:
            import json
            result = subprocess.run(base_cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            print(f"\nPlaylist: {data.get('title')}")
            for entry in data.get('entries', []):
                print(f"https://www.youtube.com/watch?v={entry['id']} - {entry.get('title', '')}")
        except Exception as e:
            print("Failed to fetch playlist data:", e)
        return

    # Download the full playlist
    try:
        subprocess.run(base_cmd, check=True)
        print("Download complete.")
    except subprocess.CalledProcessError as e:
        print("Download failed:", e)

if __name__ == "__main__":
    print("Enter YouTube playlist URL:")
    # playlist = input("Playlist URL: ").strip()
    playlist = r"https://youtube.com/playlist?list=PLoROMvodv4rPP6braWoRt5UCXYZ71GZIQ&si=zi5m4EyqIX94K7XK"
    print("Do you want to (1) download or (2) just list the videos?")
    choice = "2"
    
    download = choice == "1"
    download_youtube_playlist(playlist, download=download)


# https://www.youtube.com/watch?v=_NLHFoVNlbg AndrewNG Deeplearning
# https://youtube.com/playlist?list=PLoROMvodv4rMiGQp3WXShtMGgzqpfVfbU&si=va087M4uu7RW9JFz AndrewNG MachineLearning

# base_cmd = ["yt-dlp", "-f", "bestaudio", "--extract-audio", "--audio-format", "mp3", playlist_url]
# available formats: yt-dlp -F <video_url>

# Enter YouTube playlist URL:
# Do you want to (1) download or (2) just list the videos?

from pathlib import Path

def download_video(video_url, outdir=Path("downloads"), fmt='bestvideo+bestaudio/best'):
    """
    Download a single video using the already-imported yt_dlp as `y`.
    Example:
        download_video("https://www.youtube.com/watch?v=VIDEO_ID")
    """
    if not isinstance(outdir, Path):
        outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if not isinstance(video_url, str) or not video_url.startswith("http"):
        print("Invalid video URL.")
        return

    def _hook(d):
        status = d.get('status')
        if status == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total:
                pct = downloaded / total * 100
                print(f"Downloading: {pct:.1f}% ({downloaded}/{total} bytes)", end="\r")
        elif status == 'finished':
            print(f"\nFinished downloading: {d.get('filename')}")

    ydl_opts = {
        'format': fmt,
        'outtmpl': str(outdir / '%(title)s - %(id)s.%(ext)s'),
        'noplaylist': True,
        'progress_hooks': [_hook],
        'quiet': False,
    }

    try:
        with y.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except NameError:
        print("yt_dlp is not imported as `y`. Run `import yt_dlp as y` first.")
    except Exception as e:
        print("Download failed:", e)

# Example call:
# download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# yt-dlp -f "best[ext=mp4]" -o "%(title)s - %(id)s.%(ext)s" "https://www.youtube.com/watch?v=mMFT44ra-Rg"

# Playlist: Statistical Learning with Python
# https://www.youtube.com/watch?v=LvySJGj-88U - Statistical Learning: 1.1 Opening Remarks
# https://www.youtube.com/watch?v=9vlDVxG4ulA - Statistical Learning: 8 Years Later (Second Edition of the Course)
# https://www.youtube.com/watch?v=Igd5srPxZfU - Statistical Learning I Introducing Jonathan - Third Edition of the Course I 2023
# https://www.youtube.com/watch?v=B9s8rpdNxU0 - Statistical Learning: 1.2 Examples and Framework
# https://www.youtube.com/watch?v=ox0cKk7h4o0 - Statistical Learning: 2.1 Introduction to Regression Models
# https://www.youtube.com/watch?v=uFwbrdvrAJs - Statistical Learning: 2.2 Dimensionality and Structured Models
# https://www.youtube.com/watch?v=pvcEQfcO3pk - Statistical Learning: 2.3 Model Selection and Bias Variance Tradeoff
# https://www.youtube.com/watch?v=BMJQ3LQ_QKU - Statistical Learning: 2.4 Classification
# https://www.youtube.com/watch?v=RelOJOIKaTk - Statistical Learning: 2.Py Setting Up Python I 2023
# https://www.youtube.com/watch?v=Cv1sx_HNRHM - Statistical Learning: 2.Py Data Types, Arrays, and Basics I 2023
# https://www.youtube.com/watch?v=JykmuvCY130 - Statistical Learning: 2.Py.3 Graphics I 2023
# https://www.youtube.com/watch?v=Zcb-1JmmO_U - Statistical Learning: 2.Py Indexing and Dataframes I 2023
# https://www.youtube.com/watch?v=vCHtY6Me5FI - Statistical Learning: 3.1 Simple linear regression
# https://www.youtube.com/watch?v=3GiWpRfkSjc - Statistical Learning: 3.2 Hypothesis Testing and Confidence Intervals
# https://www.youtube.com/watch?v=o9hoLdylWKo - Statistical Learning: 3.3 Multiple Linear Regression
# https://www.youtube.com/watch?v=50sv4UTjE90 - Statistical Learning: 3.4 Some important questions
# https://www.youtube.com/watch?v=dEBQmiXv9fk - Statistical Learning: 3.5 Extensions of the Linear Model
# https://www.youtube.com/watch?v=mKalBNrxToU - Statistical Learning: 3.Py Linear Regression and statsmodels Package I 2023
# https://www.youtube.com/watch?v=pGOr3HZhUZQ - Statistical Learning: 3.Py Multiple Linear Regression Package I 2023
# https://www.youtube.com/watch?v=d0K2mDclyXM - Statistical Learning: 3.Py Interactions, Qualitative Predictors and Other Details I 2023
# https://www.youtube.com/watch?v=ju3J7iRy6xI - Statistical Learning: 4.1 Introduction to Classification Problems
# https://www.youtube.com/watch?v=kr_Be9NVXOM - Statistical Learning: 4.2 Logistic Regression
# https://www.youtube.com/watch?v=1uJVE8bkabc - Statistical Learning: 4.3 Multivariate Logistic Regression
# https://www.youtube.com/watch?v=sYDDk6R-be0 - Statistical Learning: 4.4 Logistic Regression Case Control Sampling and Multiclass
# https://www.youtube.com/watch?v=oJc2r246VoQ - Statistical Learning: 4.5 Discriminant Analysis
# https://www.youtube.com/watch?v=14JVlzWHKgk - Statistical Learning: 4.6 Gaussian Discriminant Analysis (One Variable)
# https://www.youtube.com/watch?v=aUlTqhDtpnw - Statistical Learning: 4.7 Gaussian Discriminant Analysis (Many Variables)
# https://www.youtube.com/watch?v=n8Nj64FyjSo - Statistical Learning: 4.8 Generalized Linear Models
# https://www.youtube.com/watch?v=giCZkipHEmA - Statistical Learning: 4.9 Quadratic Discriminant Analysis and Naive Bayes
# https://www.youtube.com/watch?v=wOGBlLLuc4I - Statistical Learning: 4.Py Logistic Regression I 2023
# https://www.youtube.com/watch?v=9pfRgzM1oCQ - Statistical Learning: 4.Py Linear Discriminant Analysis (LDA) I 2023
# https://www.youtube.com/watch?v=yLEx1FnYyOo - Statistical Learning: 4.Py K-Nearest Neighbors (KNN) I 2023
# https://www.youtube.com/watch?v=6eWODQJrMKs - Statistical Learning: 5.1 Cross Validation
# https://www.youtube.com/watch?v=AMfvd_hLssE - Statistical Learning: 5.2 K-fold Cross Validation
# https://www.youtube.com/watch?v=jgoa28FR__Y - Statistical Learning: 5.3 Cross Validation the wrong and right way
# https://www.youtube.com/watch?v=h_LweqiIotE - Statistical Learning: 5.4 The Bootstrap
# https://www.youtube.com/watch?v=OKREmw6YP64 - Statistical Learning: 5.5 More on the Bootstrap
# https://www.youtube.com/watch?v=oYzo95sFoSY - Statistical Learning: 5.Py Cross-Validation I 2023
# https://www.youtube.com/watch?v=1BxtC6ZOvJQ - Statistical Learning: 5.Py Bootstrap I 2023
# https://www.youtube.com/watch?v=nsv5rEV3mVI - Statistical Learning: 6.1 Introduction and Best Subset Selection
# https://www.youtube.com/watch?v=ynXq-Gw1xfE - Statistical Learning: 6.2 Stepwise Selection
# https://www.youtube.com/watch?v=c5aI9cowjRI - Statistical Learning: 6.3 Backward stepwise selection
# https://www.youtube.com/watch?v=48P-oV6cH44 - Statistical Learning: 6.4 Estimating test error
# https://www.youtube.com/watch?v=mzb5Xs58bb0 - Statistical Learning: 6.5 Validation and cross validation
# https://www.youtube.com/watch?v=lLlG5xkyqIA - Statistical Learning: 6.6 Shrinkage methods and ridge regression
# https://www.youtube.com/watch?v=0tfPuddPhEY - Statistical Learning: 6.7 The Lasso
# https://www.youtube.com/watch?v=KV1Kt6I8rYs - Statistical Learning: 6.8 Tuning parameter selection
# https://www.youtube.com/watch?v=bpto4g5l_go - Statistical Learning: 6.9 Dimension Reduction Methods
# https://www.youtube.com/watch?v=Uo19ST0IEZI - Statistical Learning: 6.10 Principal Components Regression and Partial Least Squares
# https://www.youtube.com/watch?v=EJ-haQArGzU - Statistical Learning: 6.Py Stepwise Regression I 2023
# https://www.youtube.com/watch?v=dI7xi5kRwwM - Statistical Learning: 6.Py Ridge Regression and the Lasso I 2023
# https://www.youtube.com/watch?v=F-D3lZzYn50 - Statistical Learning: 7.1 Polynomials and Step Functions
# https://www.youtube.com/watch?v=FrVaxvwCLYM - Statistical Learning: 7.2 Piecewise Polynomials and Splines
# https://www.youtube.com/watch?v=b_HSFOnrGLI - Statistical Learning: 7.3 Smoothing Splines
# https://www.youtube.com/watch?v=3aMB51GMUyQ - Statistical Learning: 7.4 Generalized Additive Models and Local Regression
# https://www.youtube.com/watch?v=_0omkfNiU2c - Statistical Learning: 7.Py Polynomial Regressions and Step Functions I 2023
# https://www.youtube.com/watch?v=C9h-o6AfNX0 - Statistical Learning: 7.Py Splines I 2023
# https://www.youtube.com/watch?v=hQx84r2maaE - Statistical Learning: 7.Py Generalized Additive Models (GAMs) I 2023
# https://www.youtube.com/watch?v=QNnayf--_yk - Statistical Learning: 8.1 Tree based methods
# https://www.youtube.com/watch?v=JaoTOfTNOVk - Statistical Learning: 8.2 More details on Trees
# https://www.youtube.com/watch?v=gLcfKSMKOb0 - Statistical Learning: 8.3 Classification Trees
# https://www.youtube.com/watch?v=_cKAxjnInfA - Statistical Learning: 8.4 Bagging
# https://www.youtube.com/watch?v=cdl4C2eCOHk - Statistical Learning: 8.5 Boosting
# https://www.youtube.com/watch?v=xWhPwHZF4c0 - Statistical Learning: 8.6 Bayesian Additive Regression Trees
# https://www.youtube.com/watch?v=AVTfC5WnDTo - Statistical Learning: 8.Py Tree-Based Methods I 2023
# https://www.youtube.com/watch?v=Op0OyOuDjcQ - Statistical Learning: 9.1 Optimal Separating Hyperplane
# https://www.youtube.com/watch?v=pjvnCEfAswc - Statistical Learning: 9.2.Support Vector Classifier
# https://www.youtube.com/watch?v=02icdqOJsH4 - Statistical Learning: 9.3 Feature Expansion and the SVM
# https://www.youtube.com/watch?v=m5d7-URGnVY - Statistical Learning: 9.4 Example and Comparison with Logistic Regression
# https://www.youtube.com/watch?v=94wKFGS4Zm4 - Statistical Learning: 9.Py Support Vector Machines I 2023
# https://www.youtube.com/watch?v=1fmHMmoa47g - Statistical Learning: 9.Py ROC Curves I 2023
# https://www.youtube.com/watch?v=jJb2qytbcNg - Statistical Learning: 10.1 Introduction to Neural Networks
# https://www.youtube.com/watch?v=ggOZuZnA6is - Statistical Learning: 10.2 Convolutional Neural Networks
# https://www.youtube.com/watch?v=Zw3L-0ZP_DA - Statistical Learning: 10.3 Document Classification
# https://www.youtube.com/watch?v=MexNVKPwu7g - Statistical Learning: 10.4 Recurrent Neural Networks
# https://www.youtube.com/watch?v=ogx1q2xBHkc - Statistical Learning: 10.5 Time Series Forecasting
# https://www.youtube.com/watch?v=07zslA8BXZY - Statistical Learning: 10.6 Fitting Neural Networks
# https://www.youtube.com/watch?v=qRHdQz_P_Lo - Statistical Learning: 10.7 Interpolation and Double Descent
# https://www.youtube.com/watch?v=-ZHEnz-emcQ - Statistical Learning: 10.Py Single Layer Model: Hitters Data I 2023
# https://www.youtube.com/watch?v=csmHZGEsONU - Statistical Learning: 10.Py Multilayer Model: MNIST Digit Data I 2023
# https://www.youtube.com/watch?v=NJ0gKDGdchQ - Statistical Learning: 10.Py Convolutional Neural Network: CIFAR Image Data I 2023
# https://www.youtube.com/watch?v=RM-MkwkGUSI - Statistical Learning: 10.Py Document Classification and Recurrent Neural Networks I 2023
# https://www.youtube.com/watch?v=7_XK7mGMm1E - Statistical Learning: 11.1 Introduction to Survival Data and Censoring
# https://www.youtube.com/watch?v=lP42Vly2MVg - Statistical Learning: 11.2 Proportional Hazards Model
# https://www.youtube.com/watch?v=ujIMPpl2Tr0 - Statistical Learning: 11.3 Estimation of Cox Model with Examples
# https://www.youtube.com/watch?v=rRYfWAsG4RI - Statistical Learning: 11.4 Model Evaluation and Further Topics
# https://www.youtube.com/watch?v=HUBmWuxu68M - Statistical Learning: 11.Py Cox Model: Brain Cancer Data I 2023
# https://www.youtube.com/watch?v=H2AE2KS89-w - Statistical Learning: 11.Py Cox Model: Publication Data I 2023
# https://www.youtube.com/watch?v=kpuQqOzQXfM - Statistical Learning: 12.1 Principal Components
# https://www.youtube.com/watch?v=O30nHhyBiAs - Statistical Learning: 12.2 Higher order principal components
# https://www.youtube.com/watch?v=ded_NQqOe7I - Statistical Learning: 12.3 k means Clustering
# https://www.youtube.com/watch?v=yktzn-Mr2Nw - Statistical Learning: 12.4 Hierarchical Clustering
# https://www.youtube.com/watch?v=MYKb5KcI55s - Statistical Learning: 12.5 Matrix Completion
# https://www.youtube.com/watch?v=InBhMLEx6sU - Statistical Learning: 12.6 Breast Cancer Example
# https://www.youtube.com/watch?v=3zpISnhksqQ - Statistical Learning: 12.Py Principal Components I 2023
# https://www.youtube.com/watch?v=xhLD4nEEVlE - Statistical Learning: 12.Py Clustering I 2023
# https://www.youtube.com/watch?v=aygQSHAbMFQ - Statistical Learning: 12.Py Application: NCI60 Data I 2023
# https://www.youtube.com/watch?v=ti9NFdjf3sM - Statistical Learning: 13.1 Introduction to Hypothesis Testing
# https://www.youtube.com/watch?v=klFG10_XajI - Statistical Learning: 13.1 Introduction to Hypothesis Testing II
# https://www.youtube.com/watch?v=-6zM6mydlfA - Statistical Learning: 13.2 Introduction to Multiple Testing and Family Wise Error Rate
# https://www.youtube.com/watch?v=xML6pCgPv2c - Statistical Learning: 13.3 Bonferroni Method for Controlling FWER
# https://www.youtube.com/watch?v=8r_pMRnG97s - Statistical Learning: 13.4 Holm's Method for Controlling FWER
# https://www.youtube.com/watch?v=4RPUrwzgO6c - Statistical Learning: 13.5 False Discovery Rate and Benjamini Hochberg Method
# https://www.youtube.com/watch?v=BwjVTbU6is0 - Statistical Learning: 13.6 Resampling Approaches
# https://www.youtube.com/watch?v=Zylc7K3hZoA - Statistical Learning: 13.6 Resampling Approaches II
# https://www.youtube.com/watch?v=SBeMlJvijbQ - Statistical Learning: 13.Py Multiple Testing I 2023
# https://www.youtube.com/watch?v=c9-zvw3AY3Q - Statistical Learning: 13.Py False Discovery Rate I 2023
# https://www.youtube.com/watch?v=mMFT44ra-Rg - Statistical Learning: 13.Py Multiple Testing and Resampling I 2023
# https://www.youtube.com/watch?v=0g-XL0WV2xo - Full Ml course by Ayush https://youtu.be/0g-XL0WV2xo?si=Zse2IlWp9LnnmaN0