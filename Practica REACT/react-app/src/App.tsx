import { Card, CardBody } from "./components/Card";
import { List } from "./components/List";

function App() {
  const list =["1", "2", "3"]
  return (
    <Card>
      <CardBody title="Hola Mundo" text="Este es el texto"></CardBody>
      <List data={list}/>
    </Card>
  );
}

export default App;
