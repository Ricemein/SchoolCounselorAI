"""
Test suite for College Admissions AI Counselor

Run with: pytest tests/
"""
import pytest
from counselor_ai.models.student import (
    StudentProfile,
    AcademicRecord,
    Extracurricular,
    ResearchExperience
)
from counselor_ai.models.university import University, Program, AdmissionStatistics


class TestAcademicRecord:
    """Test academic record model"""
    
    def test_create_basic_academic_record(self):
        """Test creating a basic academic record"""
        record = AcademicRecord(
            gpa=3.8,
            sat_total=1450,
            ap_courses=["AP CS A"],
            cs_courses=["AP CS A"]
        )
        assert record.gpa == 3.8
        assert record.sat_total == 1450
        assert len(record.ap_courses) == 1
    
    def test_gpa_validation(self):
        """Test GPA validation"""
        with pytest.raises(ValueError):
            AcademicRecord(gpa=5.0, ap_courses=[], cs_courses=[])  # GPA > 4.0
    
    def test_sat_validation(self):
        """Test SAT score validation"""
        with pytest.raises(ValueError):
            AcademicRecord(gpa=3.5, sat_total=2000, ap_courses=[], cs_courses=[])  # SAT > 1600


class TestStudentProfile:
    """Test student profile model"""
    
    @pytest.fixture
    def sample_student(self):
        """Create a sample student for testing"""
        academic_record = AcademicRecord(
            gpa=3.85,
            sat_total=1480,
            ap_courses=["AP CS A", "AP Calculus BC"],
            cs_courses=["AP CS A", "Data Structures"]
        )
        
        return StudentProfile(
            name="Test Student",
            graduation_year=2025,
            academic_record=academic_record,
            cs_interests=["AI/ML", "Robotics"]
        )
    
    def test_create_student_profile(self, sample_student):
        """Test creating a student profile"""
        assert sample_student.name == "Test Student"
        assert sample_student.graduation_year == 2025
        assert sample_student.academic_record.gpa == 3.85
    
    def test_calculate_academic_index(self, sample_student):
        """Test academic index calculation"""
        index = sample_student.calculate_academic_index()
        assert 0 <= index <= 100
        assert index > 70  # Should be relatively high for this profile
    
    def test_extracurricular_strength(self, sample_student):
        """Test extracurricular strength assessment"""
        # Initially no ECs
        assert sample_student.get_extracurricular_strength() == "needs_improvement"
        
        # Add extracurriculars
        sample_student.extracurriculars = [
            Extracurricular(
                name="Robotics Club",
                category="STEM",
                role="Captain",
                years_participated=3,
                hours_per_week=10,
                achievements=["Regional Winner"]
            ),
            Extracurricular(
                name="CS Club",
                category="STEM",
                role="President",
                years_participated=2,
                hours_per_week=5,
                achievements=["Founded club"]
            )
        ]
        
        strength = sample_student.get_extracurricular_strength()
        assert strength in ["strong", "exceptional"]
    
    def test_cs_profile_strength(self, sample_student):
        """Test CS profile strength assessment"""
        strength = sample_student.get_cs_profile_strength()
        assert strength in ["developing", "moderate", "strong", "exceptional"]
        # With AP CS A and Data Structures, should be at least moderate
        assert strength in ["moderate", "strong", "exceptional"]
    
    def test_has_research_experience(self, sample_student):
        """Test research experience detection"""
        assert not sample_student.has_research_experience()
        
        sample_student.research_experience = [
            ResearchExperience(
                title="ML Project",
                field="Computer Science",
                description="Built a CNN model",
                duration_months=6
            )
        ]
        
        assert sample_student.has_research_experience()


class TestUniversityMatching:
    """Test university matching logic"""
    
    @pytest.fixture
    def sample_university(self):
        """Create a sample university"""
        return University(
            name="Test University",
            location="City, State",
            region="Northeast",
            institution_type="public",
            size="large",
            setting="urban",
            cs_program=Program(
                name="Computer Science",
                degree_types=["BS"],
                specializations=["AI", "Systems"]
            ),
            admission_stats=AdmissionStatistics(
                acceptance_rate=0.20,
                avg_gpa=3.8,
                gpa_25th=3.6,
                gpa_75th=3.95,
                sat_avg=1400,
                sat_25th=1300,
                sat_75th=1500
            ),
            total_undergrad=20000,
            student_faculty_ratio="15:1"
        )
    
    def test_calculate_match_score(self, sample_university):
        """Test match score calculation"""
        # Strong match
        match = sample_university.calculate_match_score(3.9, 1480, "sat")
        assert match["match_type"] in ["target", "safety"]
        
        # Reach
        match = sample_university.calculate_match_score(3.4, 1250, "sat")
        assert match["match_type"] in ["reach", "high_reach"]
    
    def test_get_program_strengths(self, sample_university):
        """Test program strengths identification"""
        strengths = sample_university.get_program_strengths()
        assert isinstance(strengths, list)


class TestExtracurricular:
    """Test extracurricular model"""
    
    def test_create_extracurricular(self):
        """Test creating an extracurricular"""
        ec = Extracurricular(
            name="Robotics Team",
            category="STEM",
            role="Team Lead",
            years_participated=3,
            hours_per_week=12,
            achievements=["State Champions", "Regional Winner"]
        )
        
        assert ec.name == "Robotics Team"
        assert ec.years_participated == 3
        assert len(ec.achievements) == 2


class TestResearchExperience:
    """Test research experience model"""
    
    def test_create_research_experience(self):
        """Test creating research experience"""
        research = ResearchExperience(
            title="Machine Learning for Healthcare",
            field="Computer Science - AI",
            description="Developed CNN for medical imaging",
            duration_months=8,
            mentor="Dr. Smith",
            outcome="Published paper"
        )
        
        assert research.title == "Machine Learning for Healthcare"
        assert research.duration_months == 8
        assert research.outcome == "Published paper"


# Integration tests would require API key
class TestAgentIntegration:
    """Integration tests for agents (requires API key)"""
    
    @pytest.mark.skip(reason="Requires API key and makes real API calls")
    def test_profile_analysis_integration(self):
        """Test full profile analysis (integration test)"""
        from counselor_ai import CounselorAgent, StudentProfile
        from counselor_ai.models.student import AcademicRecord
        
        academic_record = AcademicRecord(
            gpa=3.8,
            sat_total=1450,
            ap_courses=["AP CS A"],
            cs_courses=["AP CS A"]
        )
        
        student = StudentProfile(
            name="Integration Test Student",
            graduation_year=2025,
            academic_record=academic_record,
            cs_interests=["AI/ML"]
        )
        
        agent = CounselorAgent()
        result = agent.analyze_student_profile(student)
        
        assert "objective_metrics" in result
        assert "ai_analysis" in result
        assert "quick_summary" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
