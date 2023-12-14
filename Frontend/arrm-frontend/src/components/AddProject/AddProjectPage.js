import React, { useState } from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import "./AddProject.css";
import Header from "../Header/Header.js";
import Sidebar from "../Sidebar.js";
import CloseIcon from "@mui/icons-material/Close";
import IconButton from "@mui/material/IconButton";

import {
  Container,
  Typography,
  TextField,
  TextareaAutosize,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  RadioGroup,
  FormControlLabel,
  Radio,
  Chip,
  Box,
  Checkbox,
  FormGroup,
} from "@mui/material";

const StudyAreaChip = ({ label, onDelete }) => (
  <Box
    component="li"
    sx={{
      display: "flex",
      alignItems: "start",
      justifyContent: "start",
      flexWrap: "wrap",
      gap: 0.5,
      padding: 0.5,
    }}
  >
    <Chip label={label} onDelete={onDelete} />
  </Box>
);

const StudyAreaMenuItem = ({ area, checked, onDelete }) => (
  <MenuItem key={area} value={area}>
    <Checkbox checked={checked} />
    {area}
    <IconButton
      aria-label="delete"
      size="small"
      style={{ marginLeft: "auto" }}
      onClick={(e) => {
        e.stopPropagation(); // Prevent the menu from closing
        onDelete();
      }}
    >
      <CloseIcon fontSize="small" />
    </IconButton>
  </MenuItem>
);

const AddProjectPage = () => {
  const [projectTitle, setProjectTitle] = useState("");
  const [description, setDescription] = useState("");
  const [selectedStudyAreas, setSelectedStudyAreas] = useState([]);
  const [visibility, setVisibility] = useState("public");
  const [projectHours, setProjectHours] = useState(0);
  const [useTemplate, setUseTemplate] = useState(false);
  const [milestones, setMilestones] = useState([
    { label: "Project Planning", checked: true },
    { label: "Data Collection & Processing", checked: true },
    { label: "Dissemination", checked: true },
  ]);
  const theme = createTheme();
  //TODO: Fetch Study Areas from database
  const studyAreas = ["Area 1", "Area 2", "Area 3", "Area 4","Area 1", "Area 2", "Area 3", "Area 4",];
  const [isSideNavOpen, setSideNavOpen] = useState(false);

  const handleStudyAreaChange = (event) => {
    const selectedAreas = event.target.value;
    setSelectedStudyAreas(selectedAreas);
  };

  const handleStudyAreaRemove = (removedArea) => {
    setSelectedStudyAreas((prevSelected) =>
      prevSelected.filter((area) => area !== removedArea)
    );
  };

  const handleMilestoneChange = (index) => {
    setMilestones((prevMilestones) => {
      const newMilestones = [...prevMilestones];
      newMilestones[index].checked = !newMilestones[index].checked;
      return newMilestones;
    });
  };


  const handleVisibilityChange = (event) => {
    setVisibility(event.target.value);
  };

  const handleSubmit = async (event) => {
    const formData = {
      projectTitle,
      description,
      selectedStudyAreas,
      visibility,
      projectHours,
      useTemplate,
    };
    console.log("Form submitted with data:", formData);

    // TODO: Make API request to submit formData to the server
    try {
      const response = await fetch("http://localhost:3000/add_project", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        // open success modal
        console.log("Form submitted successfully!");
      } else {
        //modal with the errors
        console.error(
          "Error submitting form:",
          response.status,
          response.statusText
        );
      }
    } catch (error) {
      // Handle network or other errors
      console.error("Error:", error.message);
    }
  };

  const handleCancel = () => {
    // TODO: Implement navigation or close the page 3-> /all_project

    console.log("Form canceled");
  };

  return (
    <ThemeProvider theme={theme}>
      <div className={`home-wrapper ${isSideNavOpen ? "side-nav-open" : ""}`}>
        {" "}
        <Header title={"Create A New Project"} />
        <Sidebar />
        <Container className="project-main-container">
          <div className="form-container-div" style={{ textAlign: "left" }}>
            <Typography
              variant="h8"
              align="center"
              style={{ fontStyle: "italic" }}
              width={700}
              padding={2}
            >
              Create a project with ARRM and you'll be able to track your
              progress throughout! Soon after project creation, ARRM can help
              you find the perfect RA for the job
            </Typography>
            <form>
              <div className="form-field">
                <InputLabel
                  htmlFor="pro_title"
                  variant="h7"
                  className="title"
                  sx={{ fontWeight: "bold", fontSize: "16px" }}
                >
                  Enter your project title here
                </InputLabel>
                <TextField
                  placeholder="Exploring policy dynamics"
                  variant="outlined"
                  size="small"
                  id="pro_title"
                  className="text-field-items"
                  value={projectTitle}
                  onChange={(e) => setProjectTitle(e.target.value)}
                  style={{
                    width: "350px",
                    marginBottom: "10px",
                    boxShadow: "4px 0px 4px rgba(0, 0.1, 0.1, 0.1)",
                    textAlign: "left",
                  }}
                />
              </div>
              <div className="form-field">
                <InputLabel
                  htmlFor="pro-descript"
                  className="title"
                  sx={{ fontWeight: "bold", fontSize: "16px" }}
                >
                  Put in a brief description of the project
                </InputLabel>
                <TextareaAutosize
                  placeholder="The project was designed for ..."
                  variant="outlined"
                  id="pro-descript"
                  className="text-field-items"
                  value={description}
                  rowsMin={4}
                  onChange={(e) => setDescription(e.target.value)}
                  style={{
                    height: "150px",
                    width: "750px",
                    marginBottom: "10px",
                    boxShadow: "4px 0px 4px rgba(0, 0.1, 0.1, 0.1)",
                  }}
                />
              </div>

             <div className="form-field">
                <InputLabel
                  htmlFor="study-area-select"
                  variant="h8"
                  size="small"
                  className="title"
                  placeholder="None Selected"
                  sx={{
                    backgroundColor: "white", 
                    padding: "0 5px",
                    zIndex: 1, 
                    
                  }}
                >
                    Select all study areas related to your project
                  </InputLabel>
                <FormControl fullWidth>
                
                  <Select
                    className="small-dropdown"
                    labelId="study-area-label"
                    id="study-area-select"
                    multiple
                    value={selectedStudyAreas}
                    onChange={handleStudyAreaChange}
                    renderValue={(selected) =>
                      selected.map((value) => (
                        <span key={value} className="study-area" >
                          {value}
                          <Button
                            type="button"
                            onClick={() => handleStudyAreaRemove(value)}
                          >
                          </Button>
                        </span>
                      ))
                    }
                  >
                    {studyAreas.map((area) => (
                      <MenuItem key={area} value={area}>
                        <Checkbox checked={selectedStudyAreas.includes(area)} />
                        {area}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </div> 
              {/* <div className="form-field">
                {" "}
                <InputLabel
                  htmlFor="study-area-select"
                  variant="h7"
                  className="title"
                  sx={{
                    fontWeight: "bold",
                    fontSize: "16px",
                    color: "black",
                    position: "absolute",
                    backgroundColor: "white",
                    padding: "0 5px",
                    zIndex: 1,
                  }}
                >
                  Select all study areas related to your project
                </InputLabel>
                <FormControl alignItems="start" fullWidth>
                  <Select
                    labelId="study-area-label"
                    id="study-area-select"
                    className="select-study-area"
                    multiple
                    value={selectedStudyAreas}
                    onChange={handleStudyAreaChange}
                    renderValue={(selected) =>
                      selected.map((value) => (
                        <StudyAreaMenuItem
                          key={value}
                          area={value}
                          checked={selectedStudyAreas.includes(value)}
                          onDelete={() => handleStudyAreaRemove(value)}
                        />
                      ))
                    }
                    sx={{ marginTop: "25px", textAlign: "start" }}
                  >
                    {studyAreas.map((area) => (
                      <MenuItem key={area} value={area}>
                        {area}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </div> */}

              <div className="form-field">
                <InputLabel
                  htmlFor="visibility"
                  variant="h7"
                  className="title"
                  sx={{ fontWeight: "bold", fontSize: "16px" }}
                >
                  Project Visibility
                </InputLabel>
                <RadioGroup
                  aria-label="Visibility"
                  name="visibility"
                  value={visibility}
                  onChange={handleVisibilityChange}
                >
                  <FormControlLabel
                    value="public"
                    control={<Radio />}
                    label="Public"
                  />
                  <FormControlLabel
                    value="private"
                    control={<Radio />}
                    label="Private"
                  />
                </RadioGroup>
              </div>

              <div className="form-field">
                <InputLabel
                  htmlFor="pro_title"
                  variant="h7"
                  className="title"
                  sx={{ fontWeight: "bold", fontSize: "16px" }}
                >
                  Enter an Estimate for the project number of hours
                </InputLabel>
                <TextField
                  placeholder="80"
                  type="number"
                  variant="outlined"
                  fullWidth
                  value={projectHours}
                  onChange={(e) => setProjectHours(e.target.value)}
                />
              </div>

              <div className="form-field">
        <FormControlLabel 
        className="title"
          control={
            <Checkbox

            style={{fontWeight:"bold"}}
              checked={useTemplate}
              onChange={() => setUseTemplate(!useTemplate)}
            />
          }
          label="Use Milestone Template"
        />

        {useTemplate && (
          <div className="auto-complete-milestones">
            {milestones.map((milestone, index) => (
              <FormControlLabel
                key={index}
                control={
                  <Checkbox
                    checked={milestone.checked}
                    onChange={() => handleMilestoneChange(index)}
                  />
                }
                label={milestone.label}
                
              />
            ))}
          </div>
        )}
      </div>

              <div className="form-field">
                <Button
                  type="submit"
                  variant="contained"
                  onSubmit={handleSubmit}
                  className="submit-button"
                >
                  Submit
                </Button>
                <Button
                  variant="contained"
                  onClick={handleCancel}
                  className="cancel-button"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </Container>
      </div>
    </ThemeProvider>
  );
};

export default AddProjectPage;
