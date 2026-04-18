def recommend_jobs(skills):
    all_jobs = [
        {
            "title": "Python Developer",
            "company": "TCS",
            "location": "Pune, India",
            "skills_needed": ["Python", "SQL", "Git"],
            "salary": "4-8 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Python+Developer&location=Pune"
        },
        {
            "title": "Data Analyst",
            "company": "Infosys",
            "location": "Bangalore, India",
            "skills_needed": ["SQL", "Excel", "Python"],
            "salary": "3-6 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Data+Analyst&location=Bangalore"
        },
        {
            "title": "Machine Learning Engineer",
            "company": "Google",
            "location": "Hyderabad, India",
            "skills_needed": ["Python", "Machine Learning", "TensorFlow"],
            "salary": "15-30 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Machine+Learning+Engineer&location=Hyderabad"
        },
        {
            "title": "Frontend Developer",
            "company": "Wipro",
            "location": "Mumbai, India",
            "skills_needed": ["JavaScript", "React", "HTML", "CSS"],
            "salary": "4-9 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Frontend+Developer&location=Mumbai"
        },
        {
            "title": "Java Developer",
            "company": "Accenture",
            "location": "Pune, India",
            "skills_needed": ["Java", "SQL", "Git"],
            "salary": "5-10 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Java+Developer&location=Pune"
        },
        {
            "title": "DevOps Engineer",
            "company": "Amazon",
            "location": "Hyderabad, India",
            "skills_needed": ["Docker", "AWS", "Python", "Git"],
            "salary": "10-20 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=DevOps+Engineer&location=Hyderabad"
        },
        {
            "title": "Full Stack Developer",
            "company": "Cognizant",
            "location": "Chennai, India",
            "skills_needed": ["JavaScript", "React", "Node.js", "SQL"],
            "salary": "6-12 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Full+Stack+Developer&location=Chennai"
        },
        {
            "title": "Data Scientist",
            "company": "Microsoft",
            "location": "Bangalore, India",
            "skills_needed": ["Python", "Machine Learning", "SQL", "TensorFlow"],
            "salary": "12-25 LPA",
            "linkedin_url": "https://www.linkedin.com/jobs/search/?keywords=Data+Scientist&location=Bangalore"
        },
    ]

    recommended = []

    for job in all_jobs:
        match_count = 0
        for skill in skills:
            if skill in job["skills_needed"]:
                match_count += 1

        if match_count > 0:
            score = (match_count / len(job["skills_needed"])) * 100
            job["match_score"] = round(score)
            recommended.append(job)

    recommended.sort(key=lambda x: x["match_score"], reverse=True)
    return recommended[:5]