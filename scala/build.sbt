name := "stack-wizard"

version := "0.1.0"

scalaVersion := "2.13.12"

libraryDependencies ++= Seq(
  "com.softwaremill.sttp.client3" %% "core" % "3.8.0",
  "org.scala-lang.modules" %% "scala-parallel-collections" % "1.0.4",
  "com.lihaoyi" %% "ujson" % "3.0.0"
)
