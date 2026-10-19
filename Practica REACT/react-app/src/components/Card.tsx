import type { ReactNode } from "react";


interface ICardBodyProps{
  title: string
  text?: string
}

export function Card(props: ICardProps) {  
  const { children } = props;
  return (
    <div className="card" style={{ width: "350px" }}>
      <div className="card-body">{children}</div>
    </div>
  );
}

interface ICardProps{
  children: ReactNode
}

export function CardBody(props: ICardBodyProps ){
  const {title, text} = props;
  return(
    <>
    <h5 className="card-title">{title}</h5>
    <p className="card-text">{text}</p>
    </>
  );
}


