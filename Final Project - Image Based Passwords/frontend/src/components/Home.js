import React, { useState, useEffect, Component } from 'react';
import {Box, Grid, GridItem, Image, Stack, Text, Input, Button, FormControl, FormLabel, useDisclosure, useBoolean} from '@chakra-ui/react';

// Globals
var selectedImagesArray = [];
var password = "";
var code = "";
var ip = "";

// Functions
function push_to_img_arry(imgName)
{
  if (!selectedImagesArray.includes(imgName))
  {
    selectedImagesArray.push(imgName);
  }
}

function remove_from_img_arry(imgName)
{
  const index = selectedImagesArray.indexOf(imgName);
  if (index > -1) {
    selectedImagesArray.splice(index, 1);
  }
}

function FindPosition(oElement)
{
  if(typeof( oElement.offsetParent ) != "undefined")
  {
    for(var posX = 0, posY = 0; oElement; oElement = oElement.offsetParent)
    {
      posX += oElement.offsetLeft;
      posY += oElement.offsetTop;
    }
      return [ posX, posY ];
    }
    else
    {
      return [ oElement.x, oElement.y ];
    }
}

function GetCoordinates(e,id,imgName)
{
  var myImg = document.getElementById(id);
  var PosX = 0;
  var PosY = 0;
  var ImgPos;
  ImgPos = FindPosition(myImg);
  if (!e) var e = window.event;
  if (e.pageX || e.pageY)
  {
    PosX = e.pageX;
    PosY = e.pageY;
  }
  else if (e.clientX || e.clientY)
    {
      PosX = e.clientX + document.body.scrollLeft
        + document.documentElement.scrollLeft;
      PosY = e.clientY + document.body.scrollTop
        + document.documentElement.scrollTop;
    }
  PosX = PosX - ImgPos[0];
  PosY = PosY - ImgPos[1];

  password = password + imgName + " " + PosX + " " + PosY + ", ";
  console.log(password);

}

function Home() {

  const [allImagesArray, setAllImagesArray] = useState([]);
  const [radii, setRadii] = useState([]);
  const [rIndex, setRIndex] = useState(0);
  const [start, setStart] = useState(false);
  const [submittedImages, setSubmittedImages] = useState(false)
  const [passwordTriedOnce, setPasswordTriedOnce] = useState(false)
  const [gotPasswordCorrect, setGotPasswordCorrect] = useState(false)
  const [submittedPassword, setSubmittedPassword] = useState(false)
  const [numberOfAttempts, setNumberOfAttempts] = useState(10);
  const [counter, setCounter] = useState(0);
  const [username, setUsername] = useState("");

  useEffect(() => {
    const data = fetch('http://' + ip + ':5000/get_password_images')
    .then(response => response.json()).then(data => setAllImagesArray(data))
    const radii = fetch('http://' + ip + ':5000/getR')
    .then(response => response.json()).then(radii => setRadii(radii))
  }, []);

    const images = allImagesArray.map(image => {
      var id_num = allImagesArray.indexOf(image);
      return (
        <Grid templateRows='repeat(2, 1fr)' templateColumns='repeat(5, 1fr)'>
        <GridItem rowSpan={1} colSpan={1}>
        <HomepageListItem id={id_num} imgName = {image} imgSrc={'http://' + ip + ':5000/get_image/'+image} imgWidth={150} imgHeight={150}/>
        </GridItem>
        </Grid>
      )
    });

    const selectedImages = selectedImagesArray.map(image => {
      var id_num = allImagesArray.indexOf(image);
      return <PasswordImage setCounter={setCounter} counter={counter} id={id_num} imgName = {image} imgSrc={'http://' + ip + ':5000/get_image/'+image} imgWidth={256} imgHeight={256}/>
    });

    function enterPassword(){
      setCounter(0);

      if (username == "")
      {
        alert("No username specified. Enter new username and password");
        password = "";
      }
      else
      {
        setPasswordTriedOnce(true);
        password = password.slice(0, -2) + ";"; // removing trailing comma
      }
    }

    function sendSignup(){
      const requestOptions = {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: username, radial_distance: radii['R'][rIndex], password: password.slice(0, -2) })
      };
      const data = fetch('http://' + ip + ':5000/signup', requestOptions)
            .then(response => {
                code = response.status;

              return response.json()})
            .then(data => {
              if (code == 201)
              {
                if (rIndex == 0)
                {
                  alert(data + "\nMake one more password!");
                }
                else
                {
                  alert(data + "\nThat's the end!");
                }
                setGotPasswordCorrect(true);

              }
              else
              {
                if(numberOfAttempts == 0)
                {
                  alert('All 10 attempts used. Choose images to make another password!');
                  reset();
                }
                else if (code == 403)
                {
                  password = "";
                  alert("Username is already taken" + "\nEnter a new username and password")
                  setPasswordTriedOnce(false);
                  setGotPasswordCorrect(false);
                  setCounter(0);
                }
                else
                {
                  password = "";
                  alert(data + "\nEnter a new password")
                  setNumberOfAttempts(numberOfAttempts - 1);
                  setPasswordTriedOnce(false);
                  setGotPasswordCorrect(false);
                  setCounter(0);
                }
              }

            });
    }

    function submitImages()
    {
      (selectedImagesArray.length < 2) ? alert("Not enough images selected") : setSubmittedImages(true);
    }

    function reset(){
      if (rIndex == 1)
      {
        alert("End of our study. Thank you for participating!")
        setGotPasswordCorrect(true);

      }
      else
      {
        setSubmittedImages(false);
        setPasswordTriedOnce(false);
        setGotPasswordCorrect(false);
        setNumberOfAttempts(10);
        password = "";
        selectedImagesArray = [];
        setCounter(0);
        setRIndex(rIndex + 1);
      }
    }

    return (

      !start ?
      <Stack>

        <Text m={10} fontSize='40px'>Image-based passwords by Rebecca Gartenberg and Mark Koszykowski </Text>
        <Text fontSize='20px'> ECE455 Cybersecurity Fall 2021</Text>
        <Text fontSize='30px'> Welcome to Picture-Password! </Text>
        <Text fontSize='20px'> We are conducting a study to determine the types of passwords that people tend to choose and compare image-based passwords to typical text-based passwords. </Text>
        <Text fontSize='20px'> Things to note: </Text>
        <Text color='blue' fontSize='20px'> - In order to participate, click start and follow the steps to choose images and create passwords based on those images </Text>
        <Text color='blue' fontSize='20px'> - You will be asked to choose 2 images and choose points on those images as your password.</Text>
        <Text color='blue' fontSize='20px'> - Once you replicate the password, you will be asked to repeat the process with another set of 2 images.</Text>
        <Text color='red' fontSize='20px'>That's it!</Text>
        <Text color='blue' fontSize='20px'> - But be careful, if you can't replicate your password you will be asked to create a new password several times until
        you either get it right or run out of attempts. </Text>
        <Text color='red' fontSize='15px'> Participation in this study is voluntary. By clicking start below you are agreeing to be part of our study. </Text>
        <Text color='red' fontSize='15px'> Our purpose is to collect data on types of passwords that people tend to choose. We appreciate if participants go through our quick demo once.</Text>
        <Text color='red' fontSize='15px'> Estimated Time: 3-6 minutes</Text>

        <Button colorScheme='blue' size='md' onClick={() => setStart(true)}>Start</Button>
      </Stack>
      :
      !submittedImages ?
      <div className="Pw">
        <Stack>
        <Text fontSize='50px'>Start by choosing 2 images that will be used for your password</Text>
        </Stack>
          <Stack m={100} direction={['column', 'row']} spacing='24px'>
          {images}
          </Stack>
          <Button size={'50px'} colorScheme='blue' variant='solid' bottom={200} onClick={() => submitImages()}>Submit Images</Button>

      </div> :
      !passwordTriedOnce ?
      <div>
        <Text fontSize='40px'>Select 6 points on the images, rememeber the order of points that you selected!</Text>
        <Stack>
        <FormControl color='red' fontSize='20px' id='username' isRequired>
          <FormLabel>Username</FormLabel>
          <Input onChange={event => setUsername(event.target.value)} w={200} h={10} placeholder={username} />
        </FormControl>
        </Stack>
        <Text color='red' fontSize='20px'>Number of points: {counter}</Text>
        <Text color='red' fontSize='20px'>Number of remaining attempts: {numberOfAttempts}</Text>
        <Stack m={0} direction={['column', 'row']} spacing='24px'>
        {selectedImages}
        </Stack>
        <Button size={'50px'} colorScheme='blue' variant='solid' bottom={100} left={350} onClick={() => enterPassword()}>Enter Password</Button>
      </div>
      :
      (numberOfAttempts > 0 && !gotPasswordCorrect) ?
      <div className="Pw">
      <Text fontSize='40px'>Reenter your password</Text>
        <Stack>
        <Text fontSize='20px'>Username: {username}</Text>
        <Text color='red' fontSize='20px'>Number of points: {counter}</Text>
        <Text color='red' fontSize='20px'>Number of remaining attempts: {numberOfAttempts}</Text>
        </Stack>
        <Stack m={0} direction={['column', 'row']} spacing='24px'>
        {selectedImages}
        </Stack>
        <Button size={'50px'} colorScheme='blue' variant='solid' bottom={100} left={350} onClick={() => sendSignup()}>Enter Password</Button>
      </div>
      :
      (rIndex == 1) ?
      <div className="Pw">
      <Text fontSize='40px'>Thank you for participating in our study!</Text>
      </div> : reset()

    )
}
export default Home;

const HomepageListItem = ({ id, imgName, imgSrc, imgWidth, imgHeight}: HomepageListItemProps) => {
  const [selected, setSelected] = useState(false);
  const [inArray, setInArray] = useState(false);

  function changeState(){

    // If selected and already in array
    if (selected && inArray)
    {
      setSelected(false);
      remove_from_img_arry(imgName);
      setInArray(false);
    }

    // If room in array, and not already in array
    else if (selectedImagesArray.length < 2 && !inArray)
    {
      setSelected(true);
      push_to_img_arry(imgName);
      setInArray(true);
    }

    else if (selectedImagesArray.length == 2 && !inArray)
    {
      alert("Select maximum 2 images");
    }
  }

    return (
          <Box>
                <Image id={id} src={imgSrc} h={imgHeight} w={imgWidth} marginLeft='auto' m={10} marginRight={['auto', 'auto', 0, 0]}
                border={selected ? '3px solid black' : ''} onClick={() => changeState()}/>
          </Box>
    );
}

const PasswordImage = ({ setCounter, counter, id, imgName, imgSrc, imgWidth, imgHeight}: PasswordImageProps) => {
    return (
          <Box>
                <Image id={id} imgName={imgName} src={imgSrc} h={imgHeight} w={imgWidth} marginLeft='auto' m={100} marginRight={['auto', 'auto', 0, 0]}
                onClick={()=>{GetCoordinates(this, id, imgName); setCounter(counter + 1);}}/>
          </Box>
    );
}
