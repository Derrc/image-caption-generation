import FileUploadButton from './components/FileUploadButton'
import { Container, Background, Text } from './Styles'
import { Card } from '@mui/material'

function App() {

  return (
      <Background>
        <Container>
          <Text fontSize='80px'> Image Caption Generator </Text>
          <FileUploadButton text='Upload'/>
        </Container>
      </Background>
  )
}

export default App